module Lexer where

import Data.List.Split
import Data.Array
import Text.Regex
import Text.Regex.Base


lexer :: String -> [String]
lexer source = filter (/= "") $ splitOneOf "\n\t " $ subRegex (mkRegex "#.*") source ""
