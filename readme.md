spapi.SPAPI 为基类，实现了请求接口的任务，要实现新的接口只需要继承它，并且实现自己的方法，通过 self.make_request 发起请求
eg:
```python
class OrderUtils(SPAPI):
    def get_order(self, order_id):
        uri = '/orders/v0/orders/{orderId}'.format(orderId=order_id)
        return self.make_request(uri=uri, method='GET')
```
响应为一个 response.SPRespone 对象，可以直接 通过 .data 来访问响应数据，original 保存了原始的 Response 响应。

因为我是在 django 中用的，缓存 sts 的地方引入了 django 这些都是问题，应该还有很多问题，太晚了，可以参考，等有时间再搞。

如果你有空也可以完善一下。或者其他志同道合的朋友可以一起维护。