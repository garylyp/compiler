class HelloWorld {

   Void main(){
       Int x;
       x = 3;
       println(new Clone().add(1,2,3,4,x));
       return;
   }

}

class Clone {
    String s;
    Int add(Int a, Int b, Int c, Int d, Int e) {
        s = "Hello";
        return a * b + c - d * -e;
    }
}
