class Main {

    Void main(){
        Int i;
        Clone c;
        Pair p;
        c = new Clone();
        c.id = 0;
        c.val = 5;
        p = new Pair();
        p.c1 = c;
        p.c2 = c.copy(4);
        i = p.getSum(p.c2.copy(4));
        println(i);
    }
}

class Clone {
    Int id;
    Int val;
    Clone copy(Int powDiff) {
        Clone c;
        c = new Clone();
        c.id = this.id + powDiff;
        c.val = 5;
        return c;
    }
    Int diff(Clone c) {                
        return c.id - this.id;
    }

    // Return the val * 10^id
    Int getId() {
        Int n;
        Int res;
        n = id;
        res = val;
        while (n > 0) {
            res = res * 10;
            n = n -1;
        }
        return res;
    }
}

class Pair {
    Clone c1;
    Clone c2;
    Int getSum(Clone c3) {
        return c1.getId() + c2.getId() + c3.getId();
    }
}
