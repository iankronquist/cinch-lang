import System.Directory
import System.Environment

import Lexer
import Parser

main = do
  let usage = "Cinch [interpret|dump|vm|compile] file"
  args <- getArgs
  if length args /= 2 then
    putStrLn usage
  else
    case (args !! 0) of
      "interpret" -> putStrLn "Not yet implemented."
      "dump"      -> dumpAst args
      "vm"        -> putStrLn "Not yet implemented."
      "compile"   -> putStrLn "Not yet implemented."

dumpAst args = do
  itExists <- doesFileExist $ args !! 1
  if itExists then do
    source <- readFile $ args !! 1
    let tokens = lexer source
    let ast = parse tokens
    putStrLn $ show ast
  else
    putStrLn $ "The file " ++ args !! 1 ++ " does not exist!"
