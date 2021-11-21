class Main {

    Void main(){
        Int i;
        i = 0;
        while (i < 10) {
            println(new Fib().eval(i));
            i = i + 1;
        }
    }
}

class Fib {
    Int a;
    Int b;
    Int eval(Int x) {
        Int temp;
        if (x < 0) {
            return -1;
        } else {
            a = 0;
            b = 1;
            while (x > 0) {
                temp = b;
                b = a + b;
                a = temp;
                x = x - 1;
            }
            return a;
        }
    }
}