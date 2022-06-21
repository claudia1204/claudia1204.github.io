---
layout: post
title:  "sass less stylus"
date:   2018-01-20 19:29:41 +0800
categories: css
---





## sass + less + stylus
1) sass
```css
h1
color: #fff
background-color: #000
```



按照sass缩进方式省去[大括号]与[分号], 且兼容css写法


2）less
```css
@base: #f938ab;

.box-shadow(@style, @c) when (iscolor(@c)) {
box-shadow:         @style @c;
-webkit-box-shadow: @style @c;
-moz-box-shadow:    @style @c;
}
.box-shadow(@style, @alpha: 50%) when (isnumber(@alpha)) {
.box-shadow(@style, rgba(0, 0, 0, @alpha));
}
.box {
color: saturate(@base, 5%);
border-color: lighten(@base, 30%);
div { .box-shadow(0 0 5px, 30%) }
}

```


引入变量：免于多处修改
混合： class之间的轻松引入和继承
嵌套：选择器之间支持嵌套


3） stylus
```css
/*style.styl*/
/*类似于CSS标准语法*/
h1 {
color: #963;
background-color:#333;
}
/*省略大括号（｛｝）*/
h1
color: #963;
background-color: #333;
/*省略大括号（｛｝）和分号（;）*/
h1
color:#963
background-color:#333

```


## 三者异同
1. 变量
   
   sass 变量必须以$开头，变量名和变量值以： 分隔
   
   less 变量必须以@开头，其余同sass
   
   stylus 不要以@声明变量



2. 作用域
   sass 包含global variables and loccal varibales [link](https://webdesign.tutsplus.com/articles/understanding-variable-scope-in-sass--cms-23498)
   local variables: are those which are declared inside a selector
   global variables: all variables defined outside of any selector are considered global variables



    Sass mixins are CSS functions that you can include whenever you want.
    The main purpose of a mixin is to make a set of properties reusable.

eg.
```css
@mixin overlay() {
   bottom: 0;
   left: 0;
   position: absolute;
   right: 0;
   top: 0;
}

 .modal-background{
   @include overlay();
   background: black;
   opacity: 0.9;
 }


 scss file ----> css file
 .modal-background{
   bottom: 0;
   left: 0;
   position: absolute;
   right: 0;
   top: 0;
   background: black;
   opacity: 0.9;
 }

```


less 和 stylus 逐级往上查找。




















