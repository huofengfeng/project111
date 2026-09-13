<template>
  <div>
    <div class="admin-card">
      <!-- 工具栏 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="data.name"
            style="width: 260px"
            placeholder="请输入名称查询"
            clearable
            @keyup.enter="load"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
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
      <el-table :data="data.tableData" stripe class="admin-table">
        <el-table-column label="用户名" prop="username" min-width="120" />
        <el-table-column label="名称" prop="name" min-width="120" />
        <el-table-column label="头像" align="center" width="80">
          <template #default="scope">
            <el-image
              v-if="scope.row.avatar"
              preview-teleported
              :src="scope.row.avatar"
              :preview-src-list="[scope.row.avatar]"
              class="avatar-thumb"
              fit="cover"
            />
            <span v-else class="avatar-empty">—</span>
          </template>
        </el-table-column>
        <el-table-column label="角色" align="center" width="100">
          <template #default="scope">
            <el-tag size="small" type="info">{{ scope.row.role || 'Admin' }}</el-tag>
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
          background
          layout="total, prev, pager, next"
          v-model:page-size="data.pageSize"
          v-model:current-page="data.pageNum"
          :total="data.total"
        />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <HeritageFormDialog
      v-model="data.formVisible"
      :title="data.form.id ? '编辑管理员' : '新增管理员'"
      confirm-text="保存"
      cancel-text="取消"
      @confirm="save"
    >
      <el-form
        ref="formRef"
        :model="data.form"
        :rules="data.rules"
        label-width="72px"
      >
        <el-form-item label="账号" prop="username">
          <el-input
            :disabled="data.form.id > 0"
            v-model="data.form.username"
            autocomplete="off"
            placeholder="请输入账号"
          />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input
            v-model="data.form.name"
            autocomplete="off"
            placeholder="请输入名称"
          />
        </el-form-item>
        <el-form-item label="头像" prop="avatar">
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
              v-if="data.form.avatar"
              :src="data.form.avatar"
              class="form-avatar-preview"
              fit="cover"
            />
            <span v-else class="upload-hint">未选择文件</span>
          </div>
        </el-form-item>
      </el-form>
    </HeritageFormDialog>
  </div>
</template>

<script setup>
import request from "@/utils/request";
import { reactive, ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { Search, Plus, EditPen, Delete } from "@element-plus/icons-vue";
import HeritageFormDialog from "@/components/HeritageFormDialog.vue";

const uploadUrl = import.meta.env.VITE_BASE_URL + '/files/upload'
const uploadHeaders = {
  Authorization: 'Bearer ' + sessionStorage.getItem('access_token')
}

const formRef = ref()
const data = reactive({
  user: JSON.parse(sessionStorage.getItem('system-user') || '{}'),
  pageNum: 1,
  pageSize: 10,
  total: 0,
  formVisible: false,
  form: {},
  tableData: [],
  name: null,
  rules: {
    username: [
      { required: true, message: '请输入账号', trigger: 'blur' }
    ],
    name: [
      { required: true, message: '请输入名称', trigger: 'blur' }
    ],
    avatar: [
      { required: true, message: '请上传头像', trigger: 'blur' }
    ],
  }
})

const load = () => {
  request.get('/admin/selectPage', {
    params: {
      pageNum: data.pageNum,
      pageSize: data.pageSize,
      name: data.name
    }
  }).then(res => {
    data.tableData = res.data?.list
    data.total = res.data?.total
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
  request.post('/admin/add', data.form).then(res => {
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
  request.put('/admin/update', data.form).then(res => {
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
  ElMessageBox.confirm('删除后数据无法恢复，确定删除吗?', '提示', { type: 'warning' }).then(() => {
    request.delete('/admin/delete/' + id).then(res => {
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
  data.pageNum = 1
  load()
}

const handleImgSuccess = (res) => {
  data.form.avatar = res.data
}

load()
</script>

<style scoped>
/* 主卡片 */
.admin-card {
  background: #faf6f0;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e0d5c5;
}

/* 工具栏 */
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
}

.toolbar-right {
  display: flex;
  align-items: center;
}

/* 表格 */
.admin-table {
  border-radius: 6px;
  overflow: hidden;
}

.admin-table :deep(th) {
  background: #f5f0e8 !important;
  color: #4a3f35 !important;
  font-weight: 600;
  font-family: 'Noto Serif SC', serif;
  font-size: 13px;
}

.admin-table :deep(td) {
  color: #5a4d3f;
  font-family: 'Noto Serif SC', serif;
}

/* 头像 */
.avatar-thumb {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  object-fit: cover;
  cursor: pointer;
  border: 1px solid #e0d5c5;
}

.avatar-empty {
  color: #c0c4cc;
  font-size: 13px;
}

/* 分页 */
.pagination-bar {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* 弹窗表单 */
.upload-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.form-avatar-preview {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  border: 1px solid #e0d5c5;
}

.upload-hint {
  color: #909399;
  font-size: 13px;
}
</style>
