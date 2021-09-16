

class Main {

    Void main(Int a){
        (new Banana()).new().a = a;   // OK
        (new Banana()).new() = a;     // NOT OK
        return;
    }

}

class Banana {
    Int a;
    Banana new() {
        return this;
    }
}

