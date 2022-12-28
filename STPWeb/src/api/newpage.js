import request from '@/utils/request'
export function newPageList() {
  return request({
    url: 'testPage/api/newpage/test',
    method: 'get'
  })
}
export function getNewPageCommit(requestBody) {
  return request({
    url: 'testPage/api/newpage/commit',
    method: 'post',
    data: requestBody
  })
}
