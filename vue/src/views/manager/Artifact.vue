<template>
  <div>
    <!-- 工具栏 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="data.name"
            style="width: 180px"
            placeholder="名称"
            clearable
            @keyup.enter="load"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select v-model="data.type" clearable placeholder="类型" style="width: 120px">
            <el-option label="瓷器" value="瓷器" />
            <el-option label="青铜器" value="青铜器" />
            <el-option label="玉器" value="玉器" />
            <el-option label="书画" value="书画" />
            <el-option label="陶器" value="陶器" />
          </el-select>
          <el-input
            v-model="data.museum"
            style="width: 160px"
            placeholder="收藏博物馆"
            clearable
            @keyup.enter="load"
          />
          <el-button type="primary" plain @click="load">查询</el-button>
          <el-button plain @click="reset">重置</el-button>
        </div>
        <div class="toolbar-right">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增
          </el-button>
        </div>
      </div>

      <!-- 表格 -->
      <el-table :data="data.tableData" stripe class="artifact-table" v-loading="data.loading" size="small">
        <el-table-column label="名称" prop="name" min-width="180" show-overflow-tooltip />
        <el-table-column label="朝代" prop="era" width="80" />
        <el-table-column label="类型" width="80" align="center">
          <template #default="scope">
            <el-tag size="small" :type="typeTagType(scope.row.type)">{{ scope.row.type || '—' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="尺寸" prop="size" min-width="160" show-overflow-tooltip />
        <el-table-column label="釉色" prop="glaze" width="80" />
        <el-table-column label="来源" prop="source" min-width="120" show-overflow-tooltip />
        <el-table-column label="馆藏地" prop="museum" min-width="100" show-overflow-tooltip />
        <el-table-column label="等级" align="center" width="80">
          <template #default="scope">
            <el-tag size="small" :type="levelTagType(scope.row.level)">{{ scope.row.level || '—' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="图片" align="center" width="80">
          <template #default="scope">
            <el-image
              v-if="scope.row.image_url"
              preview-teleported
              :src="getImageUrl(scope.row.image_url)"
              :preview-src-list="[getImageUrl(scope.row.image_url)]"
              class="img-thumb"
              fit="cover"
            />
            <span v-else class="img-empty">—</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="100" fixed="right">
          <template #default="scope">
            <el-tooltip content="编辑" placement="top">
              <el-button link type="primary" @click="handleEdit(scope.row)">
                <el-icon><EditPen /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="删除" placement="top">
              <el-button link type="danger" @click="handleDelete(scope.row.id)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination
          @current-change="load"
          @size-change="load"
          background
          layout="total, sizes, prev, pager, next"
          :page-sizes="[10, 20, 50, 100]"
          v-model:page-size="data.pageSize"
          v-model:current-page="data.pageNum"
          :total="data.total"
        />
      </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      :title="data.form.id ? '编辑文物' : '新增文物'"
      width="620px"
      v-model="data.formVisible"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="data.form"
        :rules="data.rules"
        label-width="68px"
        class="form-two-col"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="名称" prop="name">
              <el-input v-model="data.form.name" placeholder="请输入文物名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="朝代" prop="era">
              <el-select v-model="data.form.era" placeholder="请选择朝代" clearable style="width: 100%">
                <el-option label="唐" value="唐" />
                <el-option label="宋" value="宋" />
                <el-option label="元" value="元" />
                <el-option label="明" value="明" />
                <el-option label="清" value="清" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-select v-model="data.form.type" placeholder="请选择类型" clearable style="width: 100%">
                <el-option label="瓷器" value="瓷器" />
                <el-option label="青铜器" value="青铜器" />
                <el-option label="玉器" value="玉器" />
                <el-option label="书画" value="书画" />
                <el-option label="陶器" value="陶器" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="釉色" prop="glaze">
              <el-input v-model="data.form.glaze" placeholder="如：青釉、白釉" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="尺寸" prop="size">
              <el-input v-model="data.form.size" placeholder="如：高32cm 口径12cm" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="来源" prop="source">
              <el-input v-model="data.form.source" placeholder="如：出土于XX遗址" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="馆藏地" prop="museum">
              <el-input v-model="data.form.museum" placeholder="如：故宫博物院" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="等级" prop="level">
              <el-select v-model="data.form.level" placeholder="请选择等级" clearable style="width: 100%">
                <el-option label="一级文物" value="一级文物" />
                <el-option label="二级文物" value="二级文物" />
                <el-option label="三级文物" value="三级文物" />
                <el-option label="一般文物" value="一般文物" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="图片" prop="image_url" class="upload-form-item">
          <div class="upload-row">
            <el-upload
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleImgSuccess"
            >
              <el-button type="primary" plain size="small">上传图片</el-button>
            </el-upload>
            <el-image
              v-if="data.form.image_url"
              :src="getImageUrl(data.form.image_url)"
              class="form-img-preview"
              fit="cover"
            />
            <span v-else class="upload-hint">未选择文件</span>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="data.formVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import request from "@/utils/request";
import { reactive, ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { Search, Plus, EditPen, Delete } from "@element-plus/icons-vue";
import { getImageUrl } from "@/utils/imageUrl";

const uploadUrl = import.meta.env.VITE_BASE_URL + '/files/upload'
const uploadHeaders = {
  Authorization: 'Bearer ' + sessionStorage.getItem('access_token')
}

const formRef = ref()
const data = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0,
  formVisible: false,
  form: {},
  tableData: [],
  loading: false,
  name: null,
  type: null,
  museum: null,
  rules: {
    name: [{ required: true, message: '请输入文物名称', trigger: 'blur' }],
    era: [{ required: true, message: '请选择朝代', trigger: 'change' }],
    type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  }
})

const levelTagType = (level) => {
  if (level === '一级文物') return 'danger'
  if (level === '二级文物') return 'warning'
  if (level === '三级文物') return 'info'
  return ''
}

const typeTagType = (type) => {
  if (type === '瓷器') return 'warning'
  if (type === '青铜器') return 'info'
  if (type === '玉器') return 'success'
  if (type === '书画') return ''
  if (type === '陶器') return 'danger'
  return ''
}

const load = () => {
  data.loading = true
  request.get('/artifacts/selectPage', {
    params: {
      pageNum: data.pageNum,
      pageSize: data.pageSize,
      name: data.name,
      type: data.type,
      museum: data.museum,
    }
  }).then(res => {
    data.tableData = res.data?.list
    data.total = res.data?.total
  }).finally(() => {
    data.loading = false
  })
}

const handleAdd = () => {
  data.form = {}
  data.formVisible = true
}

const handleEdit = (row) => {
  data.form = JSON.parse(JSON.stringify(row))
  data.formVisible = true
}

const add = () => {
  request.post('/artifacts/add', data.form).then(res => {
    if (res.code === '200') {
      load()
      ElMessage.success('新增成功')
      data.formVisible = false
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const update = () => {
  request.put('/artifacts/update', data.form).then(res => {
    if (res.code === '200') {
      load()
      ElMessage.success('更新成功')
      data.formVisible = false
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const save = () => {
  formRef.value.validate(valid => {
    if (valid) {
      data.form.id ? update() : add()
    }
  })
}

const handleDelete = (id) => {
  ElMessageBox.confirm('删除后数据无法恢复，确定删除吗？', '提示', { type: 'warning' }).then(() => {
    request.delete('/artifacts/delete/' + id).then(res => {
      if (res.code === '200') {
        load()
        ElMessage.success('删除成功')
      } else {
        ElMessage.error(res.msg)
      }
    })
  }).catch(() => {})
}

const reset = () => {
  data.name = null
  data.type = null
  data.museum = null
  data.pageNum = 1
  load()
}

const handleImgSuccess = (res) => {
  data.form.image_url = res.data
}

load()
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.toolbar-right {
  display: flex;
  align-items: center;
}

.artifact-table {
  border-radius: 6px;
  overflow: hidden;
}

.artifact-table :deep(th) {
  background: #f5f0e8 !important;
  color: #4a3f35 !important;
  font-weight: 600;
  font-family: 'Noto Serif SC', serif;
  font-size: 13px;
}

.artifact-table :deep(td) {
  color: #5a4d3f;
  font-family: 'Noto Serif SC', serif;
}

.img-thumb {
  width: 44px;
  height: 44px;
  border-radius: 4px;
  object-fit: cover;
  cursor: pointer;
  border: 1px solid #e0d5c5;
}

.img-empty {
  color: #c0c4cc;
  font-size: 13px;
}

.pagination-bar {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* 表单两列布局 */
.form-two-col {
  padding-right: 4px;
}

.form-two-col :deep(.el-form-item) {
  margin-bottom: 16px;
}

.upload-form-item {
  margin-bottom: 0 !important;
}

.upload-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.form-img-preview {
  width: 44px;
  height: 44px;
  border-radius: 4px;
  border: 1px solid #e0d5c5;
}

.upload-hint {
  color: #909399;
  font-size: 13px;
}
</style>