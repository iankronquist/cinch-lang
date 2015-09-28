module CinchTypes where

data Tok  = Statement
          | Expression
          | Argument
          | Operator
          | BinaryExpression
          | AssignmentStatement
          | If
          | While
          | IntegerLiteral
          | FunctionCall
          | FunctionDef
          | Return
          | Identifier
          | StatementList
          deriving(Show, Eq)

-- FIXME: use Data.Tree
-- I'm doing this for practice
data Ast =  Ast {
    typ :: Tok,
    name :: String,
    children :: [Ast] 
} deriving (Show)

operators = ["+", "-", "<"]
