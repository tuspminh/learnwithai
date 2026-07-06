*Trong lập trình với Python thì Functional Programming đóng một vai trò vô cùng quan trọng và các functions trong Python là các* ***first-class citizens****. Điều đó có nghĩa là chúng ta có thể vận hành các functions giống như các objects khác:*

- *Truyền các function giống như các đối số.*
- *Gán một function cho một biến số.*
- *Return một function từ một function khác.*

*Dựa trên những điều này, Python hỗ trợ một kỹ thuật vô cùng mạnh mẽ:* ***closures****. Sau khi hiểu closures, chúng ta sẽ đi đến tiếp cận một khái niệm rất quan trọng khác —* ***decorators****. Đây là 2 khái niệm/kỹ thuật mà bất kỳ lập trình viên Python chuyên nghiệp nào cũng cần phải nắm vững.*

*Bài viết này yêu cầu kiến thức tiên quyết về scopes, namespace trong Python. Nếu bạn chưa tự tin, vui lòng đọc trước* [*Phần 1*](01_scopes.md)

## Free Variables and Closures

Nhắc lại rằng: Các functions được xác định bên trong function khác có thể truy cập các biến bên ngoài (nonlocal)

```
def outer():  
    x = 'python'  
    def inner():  
        # x trỏ đến cùng một object mà biến x bên ngoài trỏ tới.  
        print("{0} rocks!".format(x))  
    inner()  
outer() # python rocks! --> Đây được gọi là một closure.
```

Biến nonlocal **x** trong hàm inner được gọi là **free** variable. Khi chúng ta xem xét hàm inner, chúng ta thực sự đang thấy:

- hàm inner
- free variable x (đang có giá trị là ‘python’)

Xin lưu ý rằng biến x trong hàm inner không thuộc local scope của hàm đó, mà nó nằm ở một nơi khác. Nhãn x này và nhãn x thuộc hàm outer liên kết lại với nhau, được gọi là **closure**.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:875/1*3QNs0btTwQnEu0IIED_tbw.jpeg)

## Returning the inner function

Vậy điều gì sẽ xảy ra nếu như chúng ta không gọi hàm inner() bên trong hàm outer() mà thay vào đó, ta **return** nó. Khi gọi hàm outer(), hàm inner sẽ được tạo, và outer trả về hàm inner. Khi đó, **closure** nói trên vẫn đang còn tồn tại, chúng không bị mất đi. Vì vậy, khi gọi hàm outer(), trả về hàm inner, thực sự là chúng ta đang trả về một **closure**.  
Chúng ta có thể gán giá trị trả về từ hàm outer() cho một tên biến, ví dụ:

```
fn = outer() # fn là closure  
fn() # python rocks!
```

Khi chúng ta gọi hàm **fn()**, tại thời điểm đó — Python xác định giá trị của x trong một extended scope. Lưu ý rằng, hàm outer() đã chạy xong và đã kết thúc trước khi gọi hàm fn() –> scope của hàm outer đã được giải phóng. Vậy tại sao khi gọi hàm fn(), chúng ta vẫn nhận về được giá trị ‘python rocks!’ !!? –> **closure**.  
Thật magic! Để hiểu rõ hơn về closure, bạn hãy uống một chén trà rồi ngồi đọc tiếp nhé ;).

## Python Cells and Multi-Scoped Variables

Xét ví dụ đơn giản sau:

```
def outer():  
    x = 'tuanh'  
    def inner():  
        print(x)  
    return inner
```

Giá trị của biến x được chia sẻ giữa 2 scope:

- outer
- closure

Nhãn (label, name) **x** nằm trong 2 scope khác nhau nhưng luôn luôn refer tới cùng 1 giá trị. Python làm điều này bằng cách sử dụng một đối tượng trung gian, **cell object**.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:855/1*-KMpPYzsLvsco7gLgjMCvw.png)

**cell object** đóng vai trò trung gian, và x sẽ tham chiếu gián tiếp đến đối tượng có giá trị ‘tuanh’. Trên thực tế, cả 2 biến x (trong outer và inner) đều trỏ đến cùng một **cell object**. Và khi chúng ta request giá trị của biến, Python thực hiện “double-hop” để lấy về giá trị cuối cùng.  
Bây giờ, chúng ta đã hiểu tại sao khi hàm outer() kết thúc, chúng ta vẫn có thể lấy được giá trị của biến x trong hàm inner rồi chứ.

## Closures

Đến đây, chúng ta có thể nghĩ về closure như là một **function** + **extended scope** — scope mà chứa **free variables**.  
Giá trị của free variable là object mà cell trỏ tới. Mỗi khi function trong closure được gọi và free variable được tham chiếu:

- Python tìm kiếm cell object, và sau đó bất kỳ cái gì cell đang trỏ tới.

![](https://miro.medium.com/v2/resize:fit:875/1*BWiXbUzfmR_yOT_ZyZbEzw.png)

*Nguồn: Fred Baptiste (Python Deep Dive — Functional)*

## Introspection

Chúng ta tiếp tục sử dụng ví dụ như trước:

![](https://miro.medium.com/v2/resize:fit:875/1*Mw35ypEMhxFrDEywm4ye5g.jpeg)

*Nguồn: Fred Baptiste (Python Deep Dive — Functional)*

```
fn.__code__.co_freevars # trả về một tuple chứa tất cả các nhãn free variables  
fn.__closure__ # trả về một tuple nói cho chúng ta biết các cell object và các giá trị mà nó trỏ đến.
```

## Modifying free variables

Để sửa giá trị của free variables, chúng ta có thể sử dụng từ khóa nonlocal.

```
# vd.py
def counter():  
    count = 0  

    def inc():  
        nonlocal count # count lúc này là free variable  
        count += 1  
        return count  
    return inc  

fn = counter() # --> inc + count --> 0  
fn() # count --> 1  
fn() # count --> 2
```

## Multiple Instances of Closures

Nhớ rằng, mỗi khi chúng ta gọi một funcion thì một scope mới sẽ được tạo ra. Nếu function đó generates một closure, thì một closure mới cũng sẽ được tạo mỗi khi gọi function.

```
def counter():  
    count = 0  
    def inc():  
        nonlocal count  
        count += 1  
        return count  
    return inc  
    
f1 = counter() # create a scope  
f2 = counter() # another scope  
f1() # 1  
f1() # 2  
f1() # 3  
f2() # 1
```

f1 và f2 ở trên không có cùng **extended scope**, chúng là các **instances** khác nhau của closure, các cells khác nhau.

## Shared Extended Scopes

Xét ví dụ sau: vd1.py

```
def outer():  
    count = 0  
    def inc1():  
        nonlocal count # count là free variable - bound với count trong extended scope  
        count += 1  
        return count  
    def inc2():  
        nonlocal count # count là free variable - bound với cùng count trong inc1  
        count += 1  
        return count  
    return inc1, inc2 # trả về 1 tuple chứa cả 2 closures  
    
f1, f2 = outer() # tuple unpacking  
f1() # 1  
f2() # 2
```

Trong ví dụ trên, free variable **count** trong cả 2 hàm inc1 và inc2 cùng refer tới cùng 1 cell object, chúng shared extended scope.

Xét thêm một ví dụ nữa: vd2.py

```
adders = []  
for n in range(1, 4):  
    adders.append(lambda x: x + n)  
adders[0][10] # 13  
adders[1][10] # 13  
adders[2][10] # 13
```

Giải thích: Biến n trong hàm lambda trong mỗi vòng lặp thực chất là free variables, chúng shared extended scope với biến n được khởi tạo khi chạy vòng for.

- n = 1: free variable trong lambda function là biến n, nó được bound tới biến n tạo trong vòng for.
- n = 2: free variable trong lambda function là biến n, nó được bound tới (**same**) biến n tạo trong vòng for.
- n = 3: free variable trong lambda function là biến n, nó được bound tới (**same**) biến n tạo trong vòng for.

Mỗi vòng lặp, một closure được tạo ra, và mỗi free variable tương ứng trong chúng cùng trỏ với một cell object. Sau khi chạy xong vòng for, danh sách **adders** lúc này chứa 3 closures.

Nhớ rằng: biến n chỉ được “**evaluate**” khi mà hàm adders[i] được gọi. Vì cả 3 hàm trong danh sách adders đều được liên kết tới cùng 1 cell object. Nên khi chúng ta gọi adders[0] hay adders[1] thì giá trị của n lúc này đều là 3.

## Nested Closures

Chúng ta hoàn toàn cũng có thể nested các closures bên trong các closures khác.

```
def incrementer(n):  
    # inner + n --> là một closure  
    def inner(start):  
        current = start
     
        # inc + current + n --> cũng là một closure  
        def inc():  
            nonlocal current  
            current += n  
            return current  

        return inc  

    return inner  


# (inner)
fn = incrementer(2) # fn.__code__.co_freevars → ('n',), n=2

# (inc)
inc_2 = fn(100) # inc_2.__code__.co_freevars → ('current', 'n'); current = 100, n = 2

# (call inc())
inc_2() # 102, current = 102, n = 2  
inc_2() # 104, current = 104, n = 2
```
