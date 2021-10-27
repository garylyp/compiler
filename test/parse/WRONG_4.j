

class Main {

    Void main(Int a){
        (new Banana()).a = a;         // OK
        (new Banana()) = a;           // NOT OK
        return;
    }

}

class Banana {
    Int a;
    Banana new() {
        return this;
    }
}

