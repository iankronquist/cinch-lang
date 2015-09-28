import System.Directory
import System.Environment

import Lexer
import Parser

main = do
  let usage = "Cinch [lex|interpret|dump|vm|compile] file"
  args <- getArgs
  if length args /= 2 then
    putStrLn usage
  else
    case head args of
      "interpret" -> putStrLn "Not yet implemented."
      "dump"      -> dumpAst args
      "vm"        -> putStrLn "Not yet implemented."
      "compile"   -> putStrLn "Not yet implemented."
      "lex"       -> dumpTokens args
      otherwise   -> putStrLn usage


dumpTokens args = do
  itExists <- doesFileExist $ args !! 1
  if itExists then do
    source <- readFile $ args !! 1
    let tokens = lexer source
    print tokens
  else
    putStrLn $ "The file " ++ args !! 1 ++ " does not exist!"

dumpAst args = do
  itExists <- doesFileExist $ args !! 1
  if itExists then do
    source <- readFile $ args !! 1
    let tokens = lexer source
    case parse tokens of
      Nothing -> putStrLn $ "Failed to parse the file " ++ args !! 1
      Just ast -> print ast
  else
    putStrLn $ "The file " ++ args !! 1 ++ " does not exist!"
