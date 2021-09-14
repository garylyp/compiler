/*
 * Tests for return statements
 */
class Main {
    Void main() {
        return new Test().singular();
    }
}

// Testing for empty class
class Empty {}

class Test {
    Void singular() {
		test();
		return new Test();
    }

    Void emptiness() {
        return;
    }

    Void nullable() {
        t1 = null;
        return null;
    }

    Void test() {
        t1 = -6;
    }
}