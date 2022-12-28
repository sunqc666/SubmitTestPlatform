
<template>
  <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick" style="padding-left: 40px">
    <el-tab-pane label="更新Es数据" name="first">
      <div>
        <div style="margin-top:30px;">
          <el-form ref="ruleForm2" :model="ruleForm2" :rules="rules2" status-icon label-width="100px" class="demo-ruleForm">
            <el-form-item label="host" prop="host">
              <el-input v-model="ruleForm2.host" prop="host" auto-complete="off" style="width: 500px" />
            </el-form-item>
            <el-form-item label="index" prop="index">
              <el-input v-model="ruleForm2.index" auto-complete="off" style="width: 500px" />
            </el-form-item>
            <el-form-item label="type" prop="type">
              <el-input v-model="ruleForm2.type" style="width: 500px" />
            </el-form-item>
            <el-form-item label="id" prop="id">
              <el-input v-model="ruleForm2.id" style="width: 500px" />
            </el-form-item>
            <el-form-item
              v-for="(field, index) in ruleForm2.field"
              :key="field.key"
              :label="'更改字段' + index"
              :prop="'field.' + index + '.value'"
            >
              <el-input v-model="field.value1" style="width: 200px" />
              <el-select v-model="field.type" placeholder="字段类型">
                <el-option label="数字" value="number" />
                <el-option label="字符串" value="string" />
                <el-option label="布尔型" value="bool" />
              </el-select>
              <el-input v-model="field.value2" style="width: 300px" /><el-button @click.prevent="removefield(field)">删除</el-button>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm2')">提交</el-button>
              <el-button @click="addfield">新增字段</el-button>
              <el-button @click="resetForm('ruleForm2')">重置</el-button>
            </el-form-item>

          </el-form>
        </div>
        <div>

          <json-viewer
            :value="jsonData"
            :expand-depth="5"
            copyable="true"
            boxed
            sort
            style="width: auto"
          />
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="新增Es数据" name="second">新增</el-tab-pane>
    <el-tab-pane label="删除Es数据" name="third">删除</el-tab-pane>
    <el-tab-pane label="查询Es数据" name="fourth">查询</el-tab-pane>
  </el-tabs>
</template>
<script>
import Vue from 'vue'
import JsonViewer from 'vue-json-viewer'
import { updateEs } from '@/api/operateEs'

// Import JsonViewer as a Vue.js plugin
Vue.use(JsonViewer)
// or
// components: {JsonViewer}
export default {
  name: 'OperateEs',
  components: {
    JsonViewer
  },
  data() {
    // var checkHost = (rule, value, callback) => {
    //     if (!value) {
    //       return callback(new Error('年龄不能为空'));
    //     }
    return {
      ruleForm2: {
        host: '',
        index: '',
        type: '',
        id: '',
        field: [{
          value1: '',
          value2: '',
          type: ''
        }]
      },
      jsonData: {},
      rules2: {
        host: [
          { required: true, message: '请输host&port', trigger: 'blur' }
        ],
        index: [
          { required: true, message: '请输索引', trigger: 'blur' }
        ],
        id: [
          { required: true, message: '请输id', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请输type', trigger: 'blur' }
        ]
      }
    }
  },

  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          updateEs(this.ruleForm2).then(response => {
            this.jsonData = response.data
            // 如果request.js没有拦截即表示成功，给出对应提示和操作
            this.$notify({
              title: '成功',
              message: '成功',
              type: 'success'
            })
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    removefield(item) {
      var index = this.ruleForm2.field.indexOf(item)
      if (index !== -1) {
        this.ruleForm2.field.splice(index, 1)
      }
    },
    addfield() {
      this.ruleForm2.field.push({
        value1: '',
        value2: '',
        key: Date.now()
      })
    }

  }
}
</script>

<style scoped>

</style>

