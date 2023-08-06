{- |
Module          : Foreign.Pythas.Utils
Description     : Utility functions for Pythas FFI wrapping
Copyright       : (c) Simon Plakolb, 2020
License         : LGPLv3
Maintainer      : s.plakolb@gmail.com
Stability       : beta

    Utility functions used for the FFI wrapping of Pythas.
 -}
module Foreign.Pythas.Utils where

import Foreign.Pythas.HTypes (HType(..), stripIO, isIO)
import Foreign.Pythas.AST (AST(Function, Tuple, Variable))

data TypeDef = TypeDef {
    funcN :: String,
    funcT :: [HType]
    } deriving (Show, Eq)

finalizerName = (++"Finalizer")

-- FFI Export Type Construction
toFFIType :: Bool -> HType -> HType
toFFIType anyIO ht = let ht' = toFFIType' ht
        in if anyIO && (not $ isIO ht')
           then HIO ht'
           else ht'

toFFIType' :: HType -> HType
toFFIType' ht = case ht of
 HString   -> HIO $ HCWString
 HList x   -> HIO $ HCArray $ toFFIType'' x
 HTuple xs -> HIO $ HCTuple $ map toFFIType'' xs
 HFunc xs  -> undefined
 HInteger  -> HLLong
 HInt      -> HCInt
 HBool     -> HCBool
 HDouble   -> HCDouble
 HFloat    -> HCFloat
 _         -> ht
 where toFFIType'' ht = stripIO $ toFFIType' ht

fromFFIType :: HType -> HType
fromFFIType ht = case ht of
 HString    -> HIO $ HCWString
 HList x    -> HIO $ HCArray $ stripIO $ fromFFIType x
 HTuple xs  -> HIO $ HCTuple $ map (stripIO . fromFFIType) xs
 HFunc  xs  -> undefined
 HInteger   -> HLLong
 HInt       -> HCInt
 HBool      -> HCBool
 HDouble    -> HCDouble
 HFloat     -> HCFloat
 _          -> ht

fromC :: HType -> AST -> AST
fromC ht arg = case ht of
    HTuple [a,b,c,d] -> f "peekTuple4"
    HTuple [a,b,c] -> f "peekTuple3"
    HTuple [a,b] -> f "peekTuple2"
    HTuple _ -> undefined
    HString  -> f "peekCWString"
    HList _  -> f "peekArray"
    HInteger -> f "fromIntegral"
    HInt     -> f "fromIntegral"
    HBool    -> f "fromBool"
    HDouble  -> f "realToFrac"
    HFloat   -> f "realToFrac"
    _        -> arg
    where f n = Function n [arg] $ fromFFIType ht

toC :: HType -> AST -> AST
toC ht arg = case ht of
    HTuple [a,b,c,d] -> f "newTuple4"
    HTuple [a,b,c] -> f "newTuple3"
    HTuple [a,b] -> f "newTuple2"
    HTuple _ -> undefined
    HString  -> f "newCWString"
    HList _  -> f "newArray"
    HFunc _  -> undefined
    HInteger -> f "fromIntegral"
    HInt     -> f "fromIntegral"
    HBool    -> f "fromBool"
    HDouble  -> f "CDouble"
    HFloat   -> f "CFloat"
    _        -> arg
    where f n = Function n [arg] $ toFFIType' ht

free' :: HType -> AST -> Maybe AST
free' ht arg = case ht of
    HString   -> Just $ f "freeCWString"
    HList  _  -> Just $ f "freeArray"
    HTuple _  -> Just $ f "free"
    HCPtr  _  -> Just $ f "free"
    _         -> Nothing
    where f n = Function n [arg] $ HIO HUnit

varA = Variable "a"
varB = Variable "b"
varC = Variable "c"
varD = Variable "d"
tuple as = case as of
        a:b:[]   -> Tuple [varA a, varB b]
        a:b:c:[] -> Tuple [varA a, varB b, varC c]
        a:b:c:d:[] -> Tuple [varA a, varB b, varC c, varD d]

