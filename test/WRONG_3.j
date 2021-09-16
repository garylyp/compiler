

class Main {

    Void main(Int a){
        new Banana().a = a;       // OK
        new Banana().new() = a;     // NOT OK
        return;
    }

}

class Banana {
    Int a;
}

