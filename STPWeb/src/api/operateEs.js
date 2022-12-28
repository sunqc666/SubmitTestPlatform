import request from '@/utils/request'

export function updateEs(data) {
  return request({
    // url: '/vue-admin-template/user/login',
    url: '/api/operateEs',
    method: 'post',
    data
  })
}

