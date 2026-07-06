### Python Deep Dive: Hiểu closures, decorators và các ứng dụng của chúng — Phần 1

*Trong lập trình với Python thì Functional Programming đóng một vai trò vô cùng quan trọng và các functions trong Python là các* ***first-class citizens****. Điều đó có nghĩa là chúng ta có thể vận hành các functions giống như các objects khác:

- *Truyền các function giống như các đối số.*
- *Gán một function cho một biến số.*
- *Return một function từ một function khác.*

*Dựa trên những điều này, Python hỗ trợ một kỹ thuật vô cùng mạnh mẽ:* ***closures****. Sau khi hiểu closures, chúng ta sẽ đi đến tiếp cận một khái niệm rất quan trọng khác —* ***decorators****. Đây là 2 khái niệm/kỹ thuật mà bất kỳ lập trình viên Python chuyên nghiệp nào cũng cần phải nắm vững.*

## Global and Local Scopes

### Scopes and Namespaces

Khi một đối tượng được gán cho một biến (ví dụ: a = 100) thì biến đó trỏ đến một object nào đó và chúng ta nói rằng biến (name) đó được liên kết với đối tượng đó. Khi đó, object có thể được truy cập từ một số nơi trong code của chúng ta, sử dụng name (tên biến) nói trên.  
Tuy nhiên, hãy nhớ rằng tên biến và binding của nó (name và object) chỉ tồn tại trong một phần cụ thể của mã nguồn của chúng ta; phần mã nguồn mà ở đó name/binding được xác định — được gọi là **lexical scope** của các biến. Các bindings này được lưu trữ trong namespaces (mỗi scope có namespace riêng của nó).

### The Global Scope

Global scope về cơ bản là module scope. Nó chỉ nằm trong một file .py duy nhất. Trong Python thì **KHÔNG** có khái niệm global scope (qua tất cả các mô đun trong toàn bộ ứng dụng) thực sự. Chỉ có một số ngoại lệ đó là có một số đối tượng built-in, được sử dụng toàn cục, chẳng hạn như: True, False, None, dict, print.

Các biến built-in và global có thể được sử dụng bất kỳ đâu trong mô đun của chúng ta, kể cả trong các hàm.

Global scopes được nested bên trong built-in scope.

![](https://github.com/tuspminh/learnpy/blob/10d6133e7f756a0fe264597350e5efaeb995a210/py_deep_dive/closures_decorators/resources/py_global_local_scopes.png)

Nếu bạn tham chiếu một tên biến bên trong một scope và Python không tìm thấy nó trong không gian tên của scope đó –> Python sẽ tìm nó bên trong không gian tên của enclosing scope. Ví dụ trong Module1 bạn sử dụng đến nhãn **True**, Python sẽ tìm True bên trong không gian tên của built-in scope.

### The Local Scope

Khi chúng ta tạo một function, chúng ta có thể tạo các tên biến bên trong function đó (sử dụng các đối số là ví dụ). Các biến được tạo bên trong function sẽ không được tạo cho đến khi function được gọi.

Lưu ý: Giả sử chúng ta có function func1 bên trong module. Thì khi load module, Python sẽ compile mọi thứ và func1 sẽ nằm trong namespace của module đang được load. Tuy nhiên mọi thứ bên trong function sẽ chưa được tạo cho tới tận khi chúng được gọi bởi lời gọi hàm.

```
def func1(a, b):  
    # do something  
    pass
```

Mỗi khi function được gọi thì một scope mới sẽ được tạo. Và các biến được xác định bên trong function sẽ được gán cho scope đó — được gọi là **function local scope**. Lưu ý rằng đối tượng thực sự được tạo ra mà một biến trong hàm tham chiếu đến có thể khác nhau trong các lần hàm được gọi (đây là lý do tại sao đệ quy hoạt động!).

### Nested Scopes

Các scope thường được nested trong các scope khác.  
Khi yêu cầu truy cập vào một object mà một biến tham chiếu đến. Ví dụ:

```
print(a)
```

Python sẽ tìm object được bound tới biến **a** như sau:

- Đầu tiên, tìm trong local scope hiện tại. Nếu không thấy,
- Lần lượt tìm tiếp lên các scope ‘bao bọc’ scope đang tìm.

Thêm một ví dụ:

# module1.py

```
a = 10 # a thuộc global scope  
def myFunc(b):  
    print(True) # print và True thuộc built-in scope  
    print(a) # a thuộc global scope  
    print(b) # b thuộc local scope  
myFunc(300) # một local scope mới được tạo, b trỏ đến đối tượng lưu trữ 300  
myFunc('a') # thêm một local scope nữa được tạo, b trỏ đến đối tượng lưu trữ 'a'
```

### The global keyword

Khi chúng ta truy xuất một giá trị của một biến global bên trong một function. Python sẽ tìm kiếm nó theo chuỗi các không gian tên tăng dần: local -> global -> built-in

Điều gì sẽ xảy ra nếu như chúng ta sửa giá trị của một biến global bên trong một function ?

```
a = 0  
def myFunc():  
    a = 100 # Python sẽ hiểu rằng đây là biến local tại compile-time  
    print(a)  
myFunc() ## 100  
print(a) ## 0
```

Chúng ta có thể bảo Python rằng 1 biến được scoped bên trong global scope khi sử dụng nó bên trong một local scope (hàm) bằng cách sử dụng từ khóa **global**.

```
a = 0  
def myFunc():  
    global a  
    a = 100  
    print(a)  
myFunc() ## 100  
print(a) ## 100
```

### Global and Local Scoping

Khi Python gặp một định nghĩa hàm tại **compile-time**, nó sẽ **scan** bất kỳ nhãn (biến) nào có giá trị **assigned** cho chúng (**anywhere** trong function). Nếu nhãn đó không được chỉ định là **global** thì nó sẽ là **local**. Các biến được tham chiếu nhưng **not assigned** một giá trị ở bất kỳ đâu trong function sẽ **not be local**, và Python sẽ, tại **run-time**, tìm kiếm chúng trong **enclosing scopes**.  
Ví dụ 1: vidu1.py

```
a = 10  
def func1():  
    print(a) 
    # a chỉ được tham chiếu đến trong function chứ không được gán -> tại compile-time, a là non-local      
    
def func2():  
    a = 100
    # a được gán trong function -> tại compile-time, a là local  
    
def func3():  
 global a  
 a = 100 
 # a được gán và được chỉ định global -> tại compile-time, a là global
```

Ví dụ 2: vidu2.py

```
`def func4():  
    print(a)  
    a = 100 # tại compile-time, a là local  `
# khi gọi hàm func4()
# print(a) sẽ dẫn đến một run-time error bởi vì a là local,
# và chúng ta đang tham chiếu đến nó trước khi chúng ta gán một
# giá trị cho nó.

func4()
```

## Nonlocal Scopes

### Inner Functions

Chúng ta có thể định nghĩa các hàm bên trong hàm khác, như sau:

```
def outer_func():  
    # some code here  
    def inner_func():  
        # some code here  

    inner_func()  
outer_func()
```
![](https://github.com/tuspminh/learnpy/blob/10d6133e7f756a0fe264597350e5efaeb995a210/py_deep_dive/closures_decorators/resources/py_nested_local_scopes.png)
Cả hai hàm đều có quyền truy cập vào global scope, built-in scope và local scope tương ứng của chúng. Nhưng **inner** function cũng có thể truy cập vào **enclosing** scope của nó — ở đây là **outer** function.  
Scope mà không là **local**, cũng không là **global**, thì được gọi là **nonlocal scope**

### Modifying nonlocal variables

Xét ví dụ sau:

# vd.py

```
def outer_func():  
    x = 'TuAnh'  
    def inner_func():  
        x = 'HuuLinh'  
    inner_func()  
    print(x)  
outer_func() ## TuAnh
```

Khi **inner_func** được compiled, python nhìn vào phép gán tới biến **x** -> nó xác định được biến **x** là local của hàm **inner_func**. Đứng ở góc độ inner_func thì biến x trong **outer_func** là nonlocal. Hai biến này trỏ đến 2 đối tượng khác nhau, vì vậy khi gọi **outer_func()** sẽ in ra màn hình chuỗi ‘TuAnh’ thay vì ‘HuuLinh’.

Vậy làm cách nào để có thể sửa được biến **x** của hàm **outer_func** bên trong hàm **inner_func**. Rất đơn giản, giống như các biến **global**, chúng ta cần khai báo rõ ràng **nonlocal** với biến **x** bên trong hàm **inner_func**, như sau:

```
def outer_func():  
    x = 'TuAnh'  
    def inner_func():  
        nonlocal x  
        x = 'HuuLinh'  
    inner_func()  
    print(x)  
outer_func() ## HuuLinh
```

### Nonlocal Variables

Bất cứ khi nào Python nói rằng một biến là nonlocal, nó sẽ tìm kiếm trong **enclosing local scopes** lần lượt từ trong ra ngoài, cho tới khi bắt gặp lần đầu tên biến được chỉ định.  
Lưu ý: Python chỉ tìm trong local scopes, nó sẽ **KHÔNG** tìm trong **global** scope.

Xem xét các ví dụ sau đây:

# vd1.py

```
def outer():  
    x = 'tuanh'  
    def inner1():  
        x = 'python'  
        def inner2():  
            nonlocal x  
            x = 'huulinh'  
        print('inner(before): ', x)  # python  
        inner2()  
        print('inner(after): ', x)   # huulinh  
    inner1()  
    print('outer: ', x)              # tuanh  
outer()
```

# vd2.py

```
def outer():  
    x = 'tuanh'  
    def inner1():  
        nonlocal x  
        x = 'python'  
        def inner2():  
            nonlocal x  
            x = 'huulinh'  
        print('inner(before): ', x)  # python  
        inner2()  
        print('inner(after): ', x)   # huulinh  
    inner1()  
    print('outer: ', x)              # huulinh  
outer()
```

# vd3.py

```
x = 1000  
def outer():  
    x = 'tuanh'  
    def inner1():  
        nonlocal x  
        x = 'python'  
        def inner2():  
            global x  
            x = 'huulinh'  
        print('inner(before): ', x)  # python  
        inner2()  
        print('inner(after): ', x)   # python  
    inner1()  
    print('outer: ', x)              # python  
outer()  
print(x)                             # huulinh
```
