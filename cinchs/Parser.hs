module Parser where

import Data.Char
import CinchTypes

-- TODO: Write Parser monad
-- FIXME: Check that tokens like "(" and "{" are what we think and don't just 
-- ignore them

parse :: [String] -> Ast
parse tokens = do
  let (ast, _) = parseStatementList tokens
  ast


parseStatementList :: [String] -> (Ast, [String])
parseStatementList tokens = do
  let (sl, others) = parseStatementListHelper [] tokens
  (Ast { typ=StatementList, name="", children=sl }, others)

parseStatementListHelper :: [Ast] -> [String] -> ([Ast], [String])
parseStatementListHelper asts [] = (asts, [])
parseStatementListHelper asts tokens = do
  let (ast, rest) = parseStatement tokens
  parseStatementListHelper (asts++[ast]) rest


parseStatement :: [String] -> (Ast, [String])
parseStatement ("if":tokens) = parseIfStatement tokens
parseStatement ("while":tokens) = parseWhileLoop tokens
parseStatement ("function":tokens) = parseWhileLoop tokens
parseStatement ("return":tokens) = parseWhileLoop tokens
parseStatement tokens = parseExpression tokens

parseAssignment :: [String]  -> (Ast, [String])
parseAssignment tokens = do
  let (name, rest) = parseIdentifier tokens
  let (expr, others) = parseExpression $ tail rest
  (Ast { typ=AssignmentStatement, name="", children=[name, expr] }, others)

parseIfStatement :: [String] -> (Ast, [String])
parseIfStatement ("if":"(":tks) = do
  let (cond, bodytks) = parseExpression tks
  let (body, rest) = parseBlock $ tail bodytks
  (Ast { typ=If, name="", children=[cond, body] }, rest)

parseWhileLoop :: [String] -> (Ast, [String])
parseWhileLoop ("while":"(":tks) = do
  let (cond, bodytks) = parseExpression tks
  let (body, rest) = parseBlock $ tail bodytks
  (Ast { typ=If, name="", children=[cond, body] }, rest)

parseFuncDef :: [String] -> (Ast, [String])
parseFuncDef ("function":tokens) = do
  let name = head tokens
  let (argumentNames, newtoks) = parseIdentifierList $ tail $ tail tokens
  let (body, newertoks) = parseBlock $ tail newtoks
  (Ast { typ=FunctionDef, name=name, children=argumentNames++[body] }, newertoks)

parseReturnStatement :: [String] -> (Ast, [String])
parseReturnStatement ("return":rest) = do
  let (expr, others) = parseExpression rest
  (Ast { typ=Return, name="", children=[expr] }, others)

parseExpression :: [String] -> (Ast, [String])
parseExpression tokens = do
  let (first, rest) = parseExpressionHelper tokens
  if (length rest > 0) && (head rest `elem` operators) then parseBinaryExpression first rest else (first, rest)

parseExpressionHelper :: [String] -> (Ast, [String])
parseExpressionHelper (f:"(":tokens) = parseFuncCall (f:"(":tokens)
parseExpressionHelper tokens
  | all isDigit $ head tokens = parseNumber tokens
  | otherwise = parseIdentifier tokens

parseIdentifierList :: [String] -> ([Ast], [String])
parseIdentifierList tokens = parseIdentifierListHelper [] tokens

parseIdentifierListHelper :: [Ast] -> [String] -> ([Ast], [String])
parseIdentifierListHelper asts (")":rest) = (reverse asts, rest)
parseIdentifierListHelper asts tokens = do
  let (ast, rest) = parseIdentifier tokens
  (parseIdentifierListHelper (ast:asts) rest)

parseFuncCall :: [String] ->  (Ast, [String])
parseFuncCall tokens = do
  let (name, rest) = parseIdentifier tokens
  let (args, others) = parseIdentifierList $ tail rest
  (Ast { typ=FunctionCall, name="", children=name:args }, tail others)

parseNumber :: [String] ->  (Ast, [String])
parseNumber tokens = (Ast { typ=IntegerLiteral, name=head tokens, children=[] }, tail tokens)

parseIdentifier :: [String] -> (Ast, [String])
parseIdentifier tokens = (Ast { typ=Identifier, name=tokens !! 0, children=[] }, tail tokens)

parseBinaryExpression :: Ast -> [String] -> (Ast, [String])
parseBinaryExpression left tokens = do
  let foo = tail []
  let operator = head tokens
  let (right, rest) = parseExpression $ tail tokens
  (Ast { typ=BinaryExpression, name=operator, children=[right] }, rest)

parseBlock :: [String] -> (Ast, [String])
parseBlock ("{":body) = do
  let (ast, rest) = parseStatementList body
  (ast, tail rest)
