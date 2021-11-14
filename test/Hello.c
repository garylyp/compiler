#include <stdio.h>

struct A {
   int x;
   int y;
}; 

void init(struct A *obj, int a) {
   obj->x = a - 1;
   obj->y = 2 * a;
}

int foo(struct A *obj) {
   int s;
   s = obj->x * obj->y;
   return s;
}

int bar(int i) {
   if (i > 0) {
      return 0;
   }
   return 1;
}

int main() {
   struct A obj;
   init(&obj, 9);
   printf("%d\n", foo(&obj));
   return 0;
}

