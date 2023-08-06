# Baraja

Baraja is a package for emulating card deck behavior.

## Getting Started

Install baraja from [PyPi](https://pypi.python.org).

```
pip install --user baraja
```

### Create a deck of cards

```
>>> from baraja.deck import Deck
>>> from baraja.card import Card
>>> d = Deck([Card('One', 1), Card('Two', 2)])
>>> d.draw()
baraja.card.Card('Two', 2)
>>> d.draw()
baraja.card.Card('One', 1)
>>> d.draw()
>>> d.shuffle()
>>> d.draw()
baraja.card.Card('One', 1)
>>>
```

### Create a list of cards

```
>>> from baraja.card import Card
>>> cardlist = Card('one') * 2
>>> cardlist += Card('two') * 3
>>> len(cardlist)
5
>>> for c in cardlist:
...     print(c)
...
baraja.card.Card('one', None)
baraja.card.Card('one', None)
baraja.card.Card('two', None)
baraja.card.Card('two', None)
baraja.card.Card('two', None)
>>> deck.draw()
baraja.card.Card('two', None)
>>> deck.draw()
baraja.card.Card('two', None)
>>> deck.draw()
>>>
```

### Create a deck from a list of cards

```
>>> from baraja.deck import Deck
>>> deck = Deck(cardlist)
>>> deck.draw()
baraja.card.Card('one', None)
>>> deck.draw()
baraja.card.Card('two', None)
>>> deck.draw()
baraja.card.Card('one', None)
>>>
```

