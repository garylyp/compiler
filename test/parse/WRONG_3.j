

class Main {

    Void main(Int a){
        new Banana().a = a;       // OK
        new Banana().getSize() = a;     // NOT OK
        return;
    }

}

class Banana {
    Int a;
    Int getSize() {return this.a;}
}

