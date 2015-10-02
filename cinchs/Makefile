all: Cinch

Cinch:
	cabal exec ghc Cinch.hs

lint:
	cabal exec hlint Cinch.hs Parser.hs Lexer.hs CinchTypes.hs

deps:
	cabal sandbox init
	cabal install

clean:
	rm -f *.o *.hi Cinch

.PHONY: all deps clean lint
