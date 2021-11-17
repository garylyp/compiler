class HelloWorld {

   Void main(){
       Int x;
       Clone c;
       readln(x);
       println("Hello world!");
       println(-x * - x + x * 4);

       c = new Clone();
       c.a = 2;
       x = 4*4;
       x = c.a;
       println(x);
       c.b = 17 * 5;
       x = - c.b;
       println(x);
       return;
   }

}

class Clone {
    Int a;
    Int b;
}