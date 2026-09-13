import hashlib
from typing import Optional

from fastapi import APIRouter, Query

from common.result import Result
from models import Artifacts, Tombs

router = APIRouter(prefix="/knowledge-graph")

# ====== 7 类实体定义 ======
# 颜色与前端 KnowledgeGraph.vue 中图例保持一致
CATEGORY_CONFIG = {
    "artifact": {"label": "文物", "color": "#c9a84c", "size": 28},
    "dynasty":  {"label": "朝代", "color": "#3a8f7b", "size": 22},
    "museum":   {"label": "博物馆", "color": "#8b7355", "size": 20},
    "glaze":    {"label": "釉色", "color": "#c07050", "size": 20},
    "type":     {"label": "器型", "color": "#6b8fbf", "size": 20},
    "tomb":     {"label": "墓葬", "color": "#5a5a8a", "size": 24},
    "site":     {"label": "出土地", "color": "#a0a0a0", "size": 20},
}


def _make_id(category: str, value: str) -> str:
    """为实体生成唯一 ID：类别前缀 + 值的 MD5 前8位"""
    h = hashlib.md5(value.encode("utf-8")).hexdigest()[:8]
    return f"{category}_{h}"


def _make_edge_id(source: str, target: str, label: str) -> str:
    """为边生成唯一 ID"""
    raw = f"{source}->{target}->{label}"
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:8]
    return f"edge_{h}"


def _make_node(category: str, node_id: str, label: str, size: int = None) -> dict:
    """构建节点"""
    cfg = CATEGORY_CONFIG[category]
    return {
        "id": node_id,
        "label": label,
        "category": category,
        "categoryLabel": cfg["label"],
        "style": {"fill": cfg["color"]},
        "size": size or cfg["size"],
    }


def _make_edge(source: str, target: str, label: str) -> dict:
    """构建边"""
    return {
        "id": _make_edge_id(source, target, label),
        "source": source,
        "target": target,
        "label": label,
    }


def _normalize(value: Optional[str]) -> Optional[str]:
    """清洗字段值：去首尾空格，空字符串视为 None"""
    if value is None:
        return None
    v = value.strip()
    return v if v else None


@router.get("/data")
async def get_graph_data(limit: int = Query(0, description="文物数量限制，0 表示全部")):
    """
    返回知识图谱的节点和边数据。
    支持 ?limit=N 参数限制文物数量，减少图谱复杂度。
    """
    # ====== 1. 查询文物数据 ======
    query = Artifacts.all()
    if limit > 0:
        query = query.limit(limit)
    artifacts = await query

    # ====== 2. 查询墓葬数据 ======
    tombs = await Tombs.all()

    # ====== 3. 构建节点集合（去重） ======
    nodes_map = {}      # node_id -> node dict
    dynasty_set = set() # 已出现的朝代值
    museum_set = set()
    glaze_set = set()
    type_set = set()
    site_set = set()

    # ---- 文物节点 + 属性实体 ----
    for art in artifacts:
        art_id = f"artifact_{art.id}"
        nodes_map[art_id] = _make_node("artifact", art_id, art.name or f"文物#{art.id}")

        era = _normalize(art.era)
        if era and era not in dynasty_set:
            dynasty_set.add(era)
            nid = _make_id("dynasty", era)
            nodes_map[nid] = _make_node("dynasty", nid, era)

        museum = _normalize(art.museum)
        if museum and museum not in museum_set:
            museum_set.add(museum)
            nid = _make_id("museum", museum)
            nodes_map[nid] = _make_node("museum", nid, museum)

        glaze = _normalize(art.glaze)
        if glaze and glaze not in glaze_set:
            glaze_set.add(glaze)
            nid = _make_id("glaze", glaze)
            nodes_map[nid] = _make_node("glaze", nid, glaze)

        atype = _normalize(art.type)
        if atype and atype not in type_set:
            type_set.add(atype)
            nid = _make_id("type", atype)
            nodes_map[nid] = _make_node("type", nid, atype)

        source = _normalize(art.source)
        if source and source not in site_set:
            site_set.add(source)
            nid = _make_id("site", source)
            nodes_map[nid] = _make_node("site", nid, source)

    # ---- 墓葬节点 + 关联实体 ----
    for tomb in tombs:
        tomb_id = f"tomb_{tomb.id}"
        nodes_map[tomb_id] = _make_node("tomb", tomb_id, tomb.name or f"墓葬#{tomb.id}")

        era = _normalize(tomb.era)
        if era and era not in dynasty_set:
            dynasty_set.add(era)
            nid = _make_id("dynasty", era)
            nodes_map[nid] = _make_node("dynasty", nid, era)

        location = _normalize(tomb.location)
        if location and location not in site_set:
            site_set.add(location)
            nid = _make_id("site", location)
            nodes_map[nid] = _make_node("site", nid, location)

    # ====== 4. 构建边（去重） ======
    edges = []       # 按顺序保留
    edge_set = set() # 用于去重的 key

    def _add_edge(src: str, tgt: str, lbl: str):
        key = f"{src}|{tgt}|{lbl}"
        if key not in edge_set and src in nodes_map and tgt in nodes_map:
            edge_set.add(key)
            edges.append(_make_edge(src, tgt, lbl))

    # ---- 文物 → 属性 ----
    for art in artifacts:
        art_id = f"artifact_{art.id}"
        if art_id not in nodes_map:
            continue

        era = _normalize(art.era)
        if era:
            _add_edge(art_id, _make_id("dynasty", era), "所属年代")

        museum = _normalize(art.museum)
        if museum:
            _add_edge(art_id, _make_id("museum", museum), "馆藏于")

        glaze = _normalize(art.glaze)
        if glaze:
            _add_edge(art_id, _make_id("glaze", glaze), "釉色为")

        atype = _normalize(art.type)
        if atype:
            _add_edge(art_id, _make_id("type", atype), "器型为")

        source = _normalize(art.source)
        if source:
            _add_edge(art_id, _make_id("site", source), "出土于")

    # ---- 墓葬 → 属性 ----
    for tomb in tombs:
        tomb_id = f"tomb_{tomb.id}"
        if tomb_id not in nodes_map:
            continue

        era = _normalize(tomb.era)
        if era:
            _add_edge(tomb_id, _make_id("dynasty", era), "所属年代")

        location = _normalize(tomb.location)
        if location:
            _add_edge(tomb_id, _make_id("site", location), "位于")

    # ====== 5. 构建类别列表 ======
    # 只返回实际用到的类别
    used_categories = set()
    for node in nodes_map.values():
        used_categories.add(node["category"])

    categories = [
        {
            "id": cat,
            "label": CATEGORY_CONFIG[cat]["label"],
            "color": CATEGORY_CONFIG[cat]["color"],
        }
        for cat in CATEGORY_CONFIG
        if cat in used_categories
    ]

    # ====== 6. 返回 ======
    return Result.success({
        "nodes": list(nodes_map.values()),
        "edges": edges,
        "categories": categories,
    })