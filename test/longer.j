class HelloWorld {

   Void main(){
       println(new Clone().add(1,2,3,4,5,6,7));
       return;
   }

}

class Clone {
    Int a1;
    Int add(Int a, Int b, Int c, Int d, Int e, Int f, Int g) {
        a1 = one(a,b,c,d,e,f,g);        
        /*
        b1 = one(a1,b,c,d,e,f,g); 
        c1 = one(a,b1,c,d,e,f,g); 
        d1 = one(a,b,c1,d,e,f,g); 
        e1 = one(a,b,c,d1,e,f,g); 
        f1 = one(a,b,c,d,e1,f,g); 
        g1 = one(a,b,c,d,e,f1,g); 
        */
        return a1;
    }
    Int one(Int a, Int b, Int c, Int d, Int e, Int f, Int g) {
        if (1==1) {
            println(a);
            println(b);
            println(c);
            println(d);
            println(e);
            println(f);
            println(g);
            return g;
        } else {
            return -1;
        }
    }
}
