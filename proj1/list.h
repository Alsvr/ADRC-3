#include "item.h"

#ifndef _LIST_H
#define _LIST_H

typedef struct list list;

/* initialises a list. returns pointer to that list */
list *LSTinit();

/* creates new element in list. returns pointer to new in list. NULL on memory allocation error */ 													   
list *LSTadd(list *next, Item item);

/* removes to_remove from list. returns pointer to the element in list after to_remove. prev is edited so that it points to the element in list following to_remove. if to_remove is NULL, prev element will point to NULL and NULL is returned.if prev == NULL it means you want to remove the first element of the list.*/ 								   
list *LSTremove(list *prev, list *to_remove, void (*free_item)(Item)); 

/* destroys the list pointed to by lst. uses the function free_item to dealocate the memory of each item in the list */
void LSTdestroy(list *lst, void (*free_item)(Item));

/* edits current so that the following on list will be pointed to by following. returns following */ 				   
list *LSTeditfollowing(list *current, list *following);

/* returns a pointer to the item stored in element of the list pointed to by element. returns NULL if element is NULL */ 			   
Item LSTgetitem(list *element);

/* returns the address of the element that follows current in the list. if current is NULL, NULL is returned */ 									   
list *LSTfollowing(list *current);

/* applies the function pointed to by function to the item inside element. item can be used to pass information to function. returns the return value of function, which should then be properly cast to the return type of function */ 									   
Item LSTapply(list *element, Item (*function)(Item, Item), Item item); 

#endif
