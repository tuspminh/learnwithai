*Trong lập trình với Python thì Functional Programming đóng một vai trò vô cùng quan trọng và các functions trong Python là các* ***first-class citizens****. Điều đó có nghĩa là chúng ta có thể vận hành các functions giống như các objects khác:*

- *Truyền các function giống như các đối số.*
- *Gán một function cho một biến số.*
- *Return một function từ một function khác.*

*Dựa trên những điều này, Python hỗ trợ một kỹ thuật vô cùng mạnh mẽ:* ***closures****. Sau khi hiểu closures, chúng ta sẽ đi đến tiếp cận một khái niệm rất quan trọng khác —* ***decorators****. Đây là 2 khái niệm/kỹ thuật mà bất kỳ lập trình viên Python chuyên nghiệp nào cũng cần phải nắm vững.*

*Trong phần 3 này, tôi sẽ giới thiệu một số ví dụ ứng dụng closure để viết code hiệu quả hơn.*

*Bài viết này yêu cầu kiến thức tiên quyết về scopes, namespaces, closures trong Python. Nếu bạn chưa tự tin, thì nên đọc trước 2 bài viết dưới đây (theo thứ tự):*

- [*Phần 1*](https://medium.com/@huulinhcvp/python-deep-dive-hi%E1%BB%83u-closures-decorators-v%C3%A0-c%C3%A1c-%E1%BB%A9ng-d%E1%BB%A5ng-c%E1%BB%A7a-ch%C3%BAng-ph%E1%BA%A7n-1-8a371418c0cb)
- [*Phần 2*](https://medium.com/@huulinhcvp/python-deep-dive-hi%E1%BB%83u-closures-decorators-v%C3%A0-c%C3%A1c-%E1%BB%A9ng-d%E1%BB%A5ng-c%E1%BB%A7a-ch%C3%BAng-ph%E1%BA%A7n-2-7f7592634c38)

## Closure

### **Nhắc lại**

Closure có thể tránh việc lợi dụng các giá trị **global** và cung cấp một cách thức ẩn dữ liệu (**data hiding**), cung cấp một giải pháp object-oriented cho vấn đề. Khi chỉ có một vài phương thức được triển khai trong một class, thì closure có thể cung cấp một giải pháp thay thế nhưng thanh lịch hơn. Khi số lượng thuộc tính và phương thức tăng lên nhiều, thì sử dụng class sẽ phù hợp hơn. Các tiêu chí sau cho thấy closure trong Python khi một nested function có tham chiếu một giá trị trong enclosing scope:

- Tồn tại một nested function (function bên trong function khác)
- Nested function có tham chiếu đến một giá trị được khai báo bên trong enclosing function.
- Enclosing function trả về nested function (giá trị được return)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:875/1*_HJn7qPvt_EZj8XU9R8_MQ.png)

*Nguồn ảnh: Andre Ye*

## Averager

Trong ví dụ này, ta sẽ xây dựng một hàm tính giá trị trung bình của nhiều giá trị sử dụng closure. Hàm này có thể tính giá trị trung bình theo thời gian bằng cách thêm các đối số vào hàm đó mà không cần phải lặp lại việc tính tổng các giá trị trước đó.

Cách tiếp cận dễ dàng nghĩ đến nhất là sử dụng class trong Python, ở đó ta sẽ sử dụng một biến instance để lưu trữ tổng của dãy số và số số hạng. Sau đó cung cấp cho class đó một method để thêm vào 1 số hạng mới, và trả về giá trị trung bình cộng của dãy số.

```
class Averager:  
    def __init__(self):  
        self._count = 0  
        self._total = 0  

    def add(self, value):  
        self._total += value  
        self._count += 1  
        return self._total / self._count  

a = Averager()  
a.add(1) # return 1.0  
a.add(2) # return 1.5  
a.add(3) # return 2.0
```

Bằng cách sử dụng closure, ta có thể tận dụng functions trong python để xây dựng được tính năng tương tự việc sử dụng class, nhưng thanh lịch và hiệu quả hơn.

```
def averager():  
    total = 0  
    count = 0  

    def add(value):  
        nonlocal total, count  
        total += value  
        count += 1  
        return 0 if count == 0 else total / count  
    
    return add  

a = averager()  
a(1) # return 1.0  
a(2) # return 1.5  
a(3) # return 2.0
```

## Counter

Áp dụng closure, ta có thể xây dựng 1 bộ đếm, đếm số lần gọi một function mỗi khi function đó chạy. Function này có thể nhận bất kỳ đối số hoặc đối số từ khóa nào.

```
def counter(fn):  
    cnt = 0 # số lần chạy fn, khởi tạo là 0

    def inner(*args, **kwargs):  
        nonlocal cnt  
        cnt = cnt + 1  
        print('{0} has been called {1} times'.format(fn.__name__, cnt))  
        return fn(*args, **kwargs)  

    return inner
```

Giả sử ta muốn bổ sung thêm việc đếm số lần gọi hàm tính tổng 2 số:

```
def add(a, b):  
    return a + b
```

Ta có thể áp dụng closure như sau:

```
count_sum = counter(add))  
count_sum(1, 2) # sum has been called 1 times  
count_sum(3, 5) # sum has been called 2 times
```

Sở dĩ hàm **count_sum** có thể làm được như trên là bởi vì nó đang sở hữu 2 **free variables** là:

- fn: tham chiếu đến hàm add
- cnt: duy trì đếm số lần gọi hàm fn

```
count_sum.__code__.co_freevars # ('cnt', 'fn')
```

Đến đây, thay vì in ra standard output số lần gọi 1 hàm bất kỳ (hàm add chỉ là 1 ví dụ), ta có thể sử dụng 1 từ điển là global variable lưu trữ các cặp {key: value}. Ở đó, key là tên của hàm và value là số lần gọi hàm. Để làm được điều đó, ta cần sửa đổi một chút ở hàm counter bằng cách bổ sung thêm cho nó 1 đối số là tham chiếu đến từ điển lưu trữ:

```
def counter(fn, counters):  
    cnt = 0  # số lần chạy fn, khởi tạo là 0  

    def inner(*args, **kwargs):  
        nonlocal cnt  
        cnt = cnt + 1  
        counters[fn.__name__] = cnt  # counters là nonlocal  
        return fn(*args, **kwargs)  
    
    return inner

func_counters = dict() # khởi tạo từ điển

# đếm số lần chạy hàm add
counted_add = counter(add, func_counters)  
for i in range(10):  
    counted_add(i, i+1)
```

Biến func_counters là biến toàn cục, vì vậy ta có thể bổ sung thêm từ khóa là tên của hàm khác vào nó, thử 1 ví dụ, xét hàm nhân 2 số:

```
def mult(a, b):  
    return a * b  

counted_mult = counter(mult, func_counters)  
for i in range(7):  
    counted_mult(i, i)
```

Biến **func_counters** lúc này sẽ cho chúng ta biết số lần gọi hàm **add** và số lần gọi hàm **mult**

```
func_counters ## {'mult': 7, 'add': 10}
```

Cả 2 hàm **counted_add** và **counted_mult** đều đang giữ 3 **free variables**:

- fn: tham chiếu đến hàm cần đếm
- cnt: duy trì đếm số lần gọi hàm fn
- counters: tham chiếu đến từ điển lưu trữ thông tin về số lần đếm các hàm

Hãy thử nghĩ, nếu như, thay vì ta gọi:

```
counted_add = counter(add, func_counters)
```

Ta gọi như sau:

```
add = counter(add, func_counters)
```

Lúc này, ta có một hàm **add** mới, thực sự không khác hàm **add** lúc đầu về tính năng là tính tổng 2 số. Tuy nhiên sau khi gọi hàm add, lúc này ta còn nhận được thêm thông tin về số lần gọi hàm add được giữ trong biến **func_counters**.

*Như vậy, hàm counter đóng vai trò như 1 trình trang trí cho hàm add (tương tự với hàm mult), nó bổ sung thêm tính năng cho hàm add nhưng không thay đổi hành vi của hàm ađd (trả về tổng 2 số). Đây là tính chất quan trọng của decorator mà chúng ta sẽ tìm hiểu trong một bài viết sau.*

## Use Closures Skilfully

Closure là một vũ khí mạnh mẽ của Python. Người mới bắt đầu có thể gặp đôi chút khó khăn trong việc áp dụng nó trong việc viết mã. Tuy nhiên, nếu ta có thể hiểu và sử dụng nó một cách thuần thục, thì nó sẽ vô cùng hữu ích.

Trên thực tế thì decorator trong Python là một sự mở rộng của closure. Chúng ta sẽ bàn về decorator sau, nhưng ai cũng biết rằng hầu hết các framework sử dụng Python cho web development đều sử dụng decorator rất thường xuyên.

Dưới đây là 2 tips quan trọng sẽ giúp bạn sử dụng closure thuần thục:

## Sử dụng lambda function để đơn giản hóa code

Xét 1 ví dụ:

```
def outer_func():  
    name = "Tu Anh"  

    def print_name():  
        print(name)  
    
    return print_name  

f = outer_func()  
print(outer_func.__closure__) # None  
print(f.__closure__) # (<cell at 0x7f31445b2e90: str object at 0x7f314459c070>,)  
print(f.__closure__[0].cell_contents) # Tu Anh
```

Ta có thể làm cho ví dụ trên thanh lịch hơn bằng cách sử dụng lambda function:

```
def outer_func():  
    name = "Tu Anh"  

    return lambda _: print(name)  

f = outer_func()  
print(outer_func.__closure__) # None  
print(f.__closure__) # (<cell at 0x7f31445a44d0: str object at 0x7f31445b6070>,)  
print(f.__closure__[0].cell_contents) # Tu Anh
```

## Closures che giấu các biến private hiệu quả hơn

Trong Python thì không có các từ khóa built-in như là **public** hay **private** để kiểm soát khả năng truy cập của các biến. Theo quy ước, chúng ta sử dụng **double underscores** để định nghĩa một member của 1 class là private. Tuy nhiên, chúng vẫn có thể được truy cập.

Đôi khi, chúng ta cần bảo vệ mạnh mẽ hơn để ẩn một biến. Và **closures** có thể giải quyết vấn đề này. Như ví dụ ở trên, thì khó để ta có thể truy cập và thay đổi được giá trị của biến **name** trong hàm **f**. Như vậy, biến **name** dường như đã *private hơn*.

## References

[1] Andre Ye, *Essential Python Concepts & Structures Any Serious Programmer Needs to Know, Explained*

[2] Fred Baptiste, *Python Deep Dive, Part 1*

[3] Yang Zhou, *5 Levels of Understanding Closures in Python*
