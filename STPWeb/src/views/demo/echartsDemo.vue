<template>
  <div class="app-container">
    <!--    <div id="pieChartDemo"  style="width: 600px;height:400px;"></div>-->
    <div ref="pieChartDemo" style="width: 600px;height:400px;" />
    <div ref="proFileDemo" style="width: 1000px;height:400px;" />
    <div ref="ganteDemo" style="width: 1000px;height:400px;" />
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'EchartsDemo',
  mounted() {
    this.initPieChart()
    this.profile()
  },
  methods: {
    initPieChart() {
    // var chartDom = document.getElementById('pieChartDemo')
      var chartDom = this.$refs['pieChartDemo']
      var myChart = echarts.init(chartDom)
      var option = {
        title: {
          text: '大奇测试开发',
          subtext: '文章类型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 20, name: '提测平台' },
              { value: 2, name: '性能测试' },
              { value: 1, name: '流量回放' },
              { value: 3, name: '好文分享' },
              { value: 5, name: '杂谈' }
            ]
          }
        ]
      }
      option && myChart.setOption(option)
    },
    profile() {
    // var chartDom = document.getElementById('main')
      var chartDom = this.$refs['proFileDemo']
      var myChart = echarts.init(chartDom)
      var option

      var data = []
      var dataCount = 1
      var startTime = +new Date()
      var categories = ['categoryA', 'categoryB', 'categoryC', 'categoryD']
      var types = [
        { name: 'JS Heap', color: '#7b9ce1' },
        { name: 'Documents', color: '#bd6d6c' },
        { name: 'Nodes', color: '#75d874' },
        { name: 'Listeners', color: '#e0bc78' },
        { name: 'GPU Memory', color: '#dc77dc' },
        { name: 'GPU', color: '#72b362' }
      ]
      // Generate mock data
      categories.forEach(function(category, index) {
        var baseTime = startTime
        for (var i = 0; i < dataCount; i++) {
          var typeItem = types[Math.round(Math.random() * (types.length - 1))]
          var duration = Math.round(Math.random() * 10000)
          data.push({
            name: typeItem.name,
            value: [index, baseTime, (baseTime += duration), duration],
            itemStyle: {
              normal: {
                color: typeItem.color
              }
            }
          })
          baseTime += Math.round(Math.random() * 2000)
        }
      })

      console.log(data)
      function renderItem(params, api) {
        var categoryIndex = api.value(0)
        var start = api.coord([api.value(1), categoryIndex])
        var end = api.coord([api.value(2), categoryIndex])
        var height = api.size([0, 1])[1] * 0.6
        var rectShape = echarts.graphic.clipRectByRect(
          {
            x: start[0],
            y: start[1] - height / 2,
            width: end[0] - start[0],
            height: height
          },
          {
            x: params.coordSys.x,
            y: params.coordSys.y,
            width: params.coordSys.width,
            height: params.coordSys.height
          }
        )
        return (
          rectShape && {
            type: 'rect',
            transition: ['shape'],
            shape: rectShape,
            style: api.style()
          }
        )
      }
      option = {
        tooltip: {
          formatter: function(params) {
            return params.marker + params.name + ': ' + params.value[3] + ' ms'
          }
        },
        title: {
          text: 'Profile',
          left: 'center'
        },
        dataZoom: [
          {
            type: 'slider',
            filterMode: 'weakFilter',
            showDataShadow: true,
            top: 400,
            labelFormatter: ''
          },
          {
            type: 'inside',
            filterMode: 'weakFilter'
          }
        ],
        grid: {
          height: 300
        },
        xAxis: {
          min: startTime,
          scale: true,
          splitNumber: 4,
          axisLabel: {
            formatter: function(val) {
              return Math.max(0, val - startTime) + ' ms'
            }
          }
        },
        yAxis: {
          data: categories
        },
        series: [
          {
            type: 'custom',
            renderItem: renderItem,
            itemStyle: {
              opacity: 0.8
            },
            encode: {
              x: [1, 2],
              y: 0
            },
            data: [
              {
                'name': 'GPU Memory',
                'value': [
                  0,
                  1666170512648,
                  1676170512985,
                  337
                ]
              }, {
                'name': 'GPU Memory',
                'value': [
                  3,
                  1676470512648,
                  1686170512985,
                  337
                ]
              },
              {
                'name': 'Nodes',
                'value': [
                  1,
                  1666170512648,
                  1766170519134,
                  6486
                ]
              },
              {
                'name': 'Nodes',
                'value': [
                  2,
                  1666170512648,
                  1686170515939,
                  3291
                ]
              }
            ]
          }
        ]
      }
      // eslint-disable-next-line no-sequences

      option && myChart.setOption(option)
    }
  }
}
</script>

<style scoped>

</style>
