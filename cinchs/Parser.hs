module Parser where

import Data.Char
import CinchTypes

-- TODO: Write Parser monad
-- FIXME: Check that tokens like "(" and "{" are what we think and don't just 
-- ignore them

parse :: [String] -> Maybe Ast
parse tokens = case (parseStatementList tokens) of
  Just (ast, _) -> Just ast

parseStatementList :: [String] -> Maybe (Ast, [String])
parseStatementList tokens = case parseStatementListHelper [] tokens of
  Nothing -> Nothing
  Just (sl, others) -> Just (Ast { typ=StatementList, name="", children=sl }, others)

parseStatementListHelper :: [Ast] -> [String] -> Maybe ([Ast], [String])
parseStatementListHelper asts [] = Just (asts, [])
parseStatementListHelper asts tokens = case parseStatement tokens of
  Nothing -> Nothing
  Just (ast, rest) -> parseStatementListHelper (asts++[ast]) rest


parseStatement :: [String] -> Maybe (Ast, [String])
parseStatement ("if":"(":tokens) = parseIfStatement tokens
parseStatement ("while":"(":tokens) = parseWhileLoop tokens
parseStatement ("function":"(":tokens) = parseWhileLoop tokens
parseStatement ("return":tokens) = parseWhileLoop tokens
parseStatement tokens = parseExpression tokens

parseAssignment :: [String]  -> Maybe (Ast, [String])
parseAssignment tokens = case parseIdentifier tokens of
  Nothing -> Nothing
  Just (name, ("=":rest)) -> case parseExpression rest of
    Nothing -> Nothing
    Just (expr, others) -> Just (Ast { typ=AssignmentStatement, name="", children=[name, expr] }, others)
  otherwise -> Nothing

parseIfStatement :: [String] -> Maybe (Ast, [String])
parseIfStatement tks = case parseExpression tks of
  Nothing -> Nothing
  Just (cond, ("{":body)) -> case parseBlock body of
    Nothing -> Nothing
    Just (body, ("}":rest)) -> Just (Ast { typ=If, name="", children=[cond, body] }, rest)
    otherwise -> Nothing

parseWhileLoop :: [String] -> Maybe (Ast, [String])
parseWhileLoop tks = case parseExpression tks of
  Nothing -> Nothing
  Just (cond, ("{":body)) -> case parseBlock body of
    Nothing -> Nothing
    Just (body, ("}":rest)) -> Just (Ast { typ=While, name="", children=[cond, body] }, rest)
    otherwise -> Nothing

parseFuncDef :: [String] -> Maybe (Ast, [String])
parseFuncDef ("function":name:(")":"{":tokens)) = case (parseIdentifierList tokens) of
  Nothing -> Nothing
  Just (argumentNames, ("}":newtoks)) -> case (parseBlock newtoks) of
    Nothing -> Nothing
    Just (body, newertoks) -> Just (Ast { typ=FunctionDef, name=name, children=argumentNames++[body] }, newertoks)
  otherwise -> Nothing
parseFuncDef otherwise = Nothing

parseReturnStatement :: [String] -> Maybe (Ast, [String])
parseReturnStatement ("return":rest) = case (parseExpression rest) of
  Nothing -> Nothing
  Just (expr, others) -> Just (Ast { typ=Return, name="", children=[expr] }, others)

parseExpression :: [String] -> Maybe (Ast, [String])
parseExpression tokens = case (parseExpressionHelper tokens) of
  Nothing -> Nothing
  Just (first, (op:rest)) -> if (op `elem` operators) then
      parseBinaryExpression first (op:rest)
    else
      Just (first, rest)
  Just (first, []) -> Just (first, [])
  otherwise -> Nothing

parseExpressionHelper :: [String] -> Maybe (Ast, [String])
parseExpressionHelper (f:"(":tokens) = parseFuncCall (f:"(":tokens)
parseExpressionHelper tokens
  | all isDigit $ head tokens = parseNumber tokens
  | otherwise = parseIdentifier tokens

parseIdentifierList :: [String] -> Maybe ([Ast], [String])
parseIdentifierList = parseIdentifierListHelper []

parseIdentifierListHelper :: [Ast] -> [String] -> Maybe ([Ast], [String])
parseIdentifierListHelper asts (")":rest) = Just (reverse asts, rest)
parseIdentifierListHelper asts tokens = case (parseIdentifier tokens) of
  Nothing -> Nothing
  Just (ast, rest) -> parseIdentifierListHelper (ast:asts) rest

parseFuncCall :: [String] ->  Maybe (Ast, [String])
parseFuncCall tokens = case (parseIdentifier tokens) of
  Nothing -> Nothing
  Just (name, rest) -> case (parseIdentifierList $ tail rest) of
    Nothing -> Nothing
    Just (args, others) -> Just (
      Ast { typ=FunctionCall, name="", children=name:args },
      tail others)

parseNumber :: [String] ->  Maybe (Ast, [String])
parseNumber tokens = Just (Ast { typ=IntegerLiteral, name=head tokens, children=[] }, tail tokens)

parseIdentifier :: [String] -> Maybe (Ast, [String])
parseIdentifier tokens = Just (Ast { typ=Identifier, name=head tokens, children=[] }, tail tokens)

parseBinaryExpression :: Ast -> [String] -> Maybe (Ast, [String])
parseBinaryExpression left (operator:tokens) = do
  case (parseExpression tokens) of
    Nothing -> Nothing
    Just (right, rest) -> Just (Ast { typ=BinaryExpression, name=operator, children=[right] }, rest)

parseBlock :: [String] -> Maybe (Ast, [String])
parseBlock ("{":body) = do
  let sl = parseStatementList body
  case sl of
    Nothing -> Nothing
    Just (ast, rest) -> Just (ast, tail rest)
