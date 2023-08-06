{- |
Module          : Foreign.Pythas.HTypes
Description     : Sum type wrapper for supported types
Copyright       : (c) Simon Plakolb, 2020
License         : LGPLv3
Maintainer      : s.plakolb@gmail.com
Stability       : beta

    Provides a sum type and accompanying functions to
    represent all Haskell types supported by Pythas on
    a data level.
 -}
module Foreign.Pythas.HTypes (HType(..), htype, stripIO, isIO) where

import Text.Parsec ((<|>), unexpected, try, skipMany)
import qualified Text.Parsec.Char as PC (string)
import Text.Parsec.String (Parser)

data HType
   = HUnit
   | HBool
   | HCBool
   | HChar
   | HCChar
   | HWChar
   | HSChar
   | HUChar
   | HShort
   | HUShort
   | HCInt
   | HCUInt
   | HLong
   | HULong
   | HLLong
   | HULLong
   | HFloat
   | HDouble
   | HCFloat
   | HCDouble
   | HInt
   | HInteger
   | HString
   | HCWString
   | HIO HType
   | HList HType
   | HTuple [HType]
   | HFunc [HType]
   | HCTuple [HType]
   | HCFunc [HType]
   | HCArray HType
   | HCList HType
   | HCPtr HType -- TODO constrain HTypes available (only Storable ones)
   deriving (Show, Eq)

htype = foldr (<|>) (unexpected "invalid type") types
 where types = [char, cchar, schar, uchar, short, ushort
               , int32, uint32, long, ulong, float
               , double, bool, integer, int, cwstring
               , cfloat, cdouble, string]

makeParser :: HType -> [String] -> Parser HType
makeParser t ss = foldr ((<|>) . try . PC.string) (unexpected "invalid type") ss
               >> return t

mp = makeParser
bool = mp HBool ["Bool"]
char = mp HChar ["Char"]
cchar = mp HCChar ["CChar","Int8"]
schar = mp HSChar ["CSChar","Int8"]
uchar = mp HUChar ["CUChar", "Word8"]
short = mp HShort ["CShort", "Int16"]
ushort = mp HUShort ["CUShort", "Word16"]
int32 = mp HCInt ["CInt","Int32"]
uint32 = mp HCUInt ["CUInt", "Word32"]
long = mp HLong ["CLong", "Int64"]
ulong = mp HULong ["CULong", "Word64"]
float = mp HFloat ["Float"]
double = mp HDouble ["Double"]
cfloat = mp HCFloat ["CFloat"]
cdouble = mp HCDouble ["CDouble"]
string = mp HString ["[Char]","String"]
int = mp HInt ["Int"]
integer = mp HInteger ["Integer"]
cwstring = mp HCWString ["CWString", "Ptr CWchar"]

isIO :: HType -> Bool
isIO (HIO _) = True
isIO _ = False

stripIO :: HType -> HType
stripIO ht = case ht of
    HIO ht -> ht
    _      -> ht

