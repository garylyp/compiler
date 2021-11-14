class HelloWorld {

   Void main(){
       println(new Clone().add(1,2,3,4,5));
       return;
   }

}

class Clone {
    Int add(Int a, Int b, Int c, Int d, Int e) {
        return a * b + c - d * e;
    }
}
