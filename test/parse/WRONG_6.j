

class Main {

    Void main(Int a){
        (new Banana()).newBanana();   // OK
        (new Banana());               // NOT OK
        return;
    }

}

class Banana {
    Int a;
    Banana newBanana() {
        return this;
    }
}

