class Main {

    Void main(){
        String s;
        Clone c;
        Int x;
        x = 10;
        c = new Clone();
        c.val = x;
        c.bl = false;

        c.copy().parent = c;
        c = c.copy();

        c.bl = false;
        c = c.copy().copy().copy();
        
        x = c.val;
        while (x > 0) {
            x = x - 1;
            println(x);
            c.doNothing(c);
        }


        return;
    }
}

class Clone {
    Int val;
    Clone parent;
    Bool bl;

    Clone copy() {
        Clone c;
        c = new Clone();
        c.val = this.val;
        c.parent = this;
        c.bl = this.bl;
        return c;
    }
    Void doNothing(Clone c) {
        return;
    }
}