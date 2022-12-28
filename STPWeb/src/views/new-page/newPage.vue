<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%"
      :row-class-name="tableRowClassName"
    >
      <el-table-column
        prop="date"
        label="日期"
        width="180"
      />
      <el-table-column
        prop="name"
        label="姓名"
        width="180"
      />
      <el-table-column
        prop="address"
        label="地址"
      />
    </el-table>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="审批人">
        <el-input v-model="formInline.user" placeholder="审批人" />
      </el-form-item>
      <el-form-item label="活动区域">
        <el-select v-model="formInline.region" placeholder="活动区域">
          <el-option label="上海" value="shanghai" />
          <el-option label="北京" value="beijing" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
// eslint-disable-next-line no-unused-vars
import { newPageList, getNewPageCommit } from '@/api/newpage'

export default {
  name: 'NewPage',
  data() {
    return { formInline: {
      user: '',
      region: ''
    },
    tableData: []
    }
  },
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getNewPageList()
  },
  methods: {
    getNewPageList() {
      newPageList().then(response => {
        // console.log(response.data)
        this.tableData = response.data
      })
    },
    onSubmit() {
      console.log('submit!')
      getNewPageCommit(this.formInline).then(response => {
        console.log(JSON.parse(response.data))
        const user = JSON.parse(response.data).user
        const region = JSON.parse(response.data).region
        // 如果request.js没有拦截即表示成功，给出对应提示和操作
        this.$notify({
          title: '提交成功',
          message: user + region,
          type: 'success'
        })
      })
    }
  }
}
</script>
