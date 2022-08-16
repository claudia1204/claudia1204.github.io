---
layout: post
title:  "闭包"
date:   2022-07-16 22:29:41 +0800
categories: closure
---

## 闭包概念
在一个内部函数中，对外部作用域的变量进行引用，并且一般外部函数的返回值为内部函数，那么内部函数就被认为是闭包

## 闭包的作用
  1. 可以读取函数内部的变量 
  2. 让内部变量始终保持在内存中

  
## 闭包demo
### js demo：
```javascript
//此处可以将闭包理解成能够读取其它函数内部变量的函数。f2就是闭包
function f1(){
    var n=110;
    function f2(){
        console.log(n) //子对象可以访问父对象的所有属性。父对象不能访问子对象属性
        n = n+1
    }
    return f2
}
f1_return = f1()
f1_return()
f1_return()
```

### python demo
```python
def f1():
    n = 110
    def f2():
        nonlocal n
        print(n)
        n = n + 1

    return f2

f1_return = f1()
f1_return()
f1_return()
```

## 闭包应用场景
  计数器
  封装对象的私有属性和方法

```javascript
function Person(name){
    var name=name;
    var age=20;
    function getAge(){
        return age
    }
    function setAge(n){
        age = n
    }
    return {
        name: name,
        age: age,
        getAge: getAge,
        setAge: setAge
    }
}
person = Person("ladygaga")
console.log(person.getAge())
person.setAge(50)
console.log(person.getAge())
```

### java demo
``` java
public class Outer {
    private int age;
    public Outer(int age){
        this.age = age;
    }
    class Inner {
        public void setAge(int age){
            Outer.this.age = age;
        }
		public int getAge(){
            return Outer.this.age;
        }
    }
}


public class Main {
  public static void main(String[] args) {
    Outer myOuter = new Outer(1);
    Outer.Inner myInner = myOuter.new Inner();
    System.out.println(myInner.getAge());
    myInner.setAge(20);
    System.out.println(myInner.getAge());
  }
}
```



## 使用闭包需要注意的事情
  1. 内存消耗大，不能滥用
  2. 闭包会改变父函数内部变量的值，使用时要小心