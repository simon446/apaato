# apaato
This application allows you to see the probability of you getting an accommodation on studentbostader.se. The probabilities are based on a simulation of how they probably distribute the accommodations.

## Example
![Example image](https://i.imgur.com/RSjVqbP.png)

## Installing

```
# clone repository
git clone https://github.com/l0f3n/apaato.git

# install package
pip3 install ./apaato/
```

## Using

The three main commands are listed below.

`apaato load`: loads all accommodations into a database.

`apaato list`: lists all accommodations.

`apaato prob`: lists the probabilities of getting the accommodation.

`apaato mont`: monitor accommodations, print when an accommodation direct matches critera.

For more options on each of these commands, use the `-h` flag.
