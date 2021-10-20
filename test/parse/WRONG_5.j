

class Main {

    Void main(Int a){
        (new Banana()).newBanana().a = a;   // OK
        (new Banana()).newBanana() = a;     // NOT OK
        return;
    }

}

class Banana {
    Int a;
    Banana newBanana() {
        return this;
    }
}

