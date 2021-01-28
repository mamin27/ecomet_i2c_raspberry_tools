unit ecomet_regex;

{$mode objfpc}{$H+}

interface

type

  TParts = array [1..100] of String;

 function StringPart(Source: string; seperator: char; Index: integer): string;
 function StringParts(Source: string; seperator: char): integer;
 function StringSplit(Source: string; seperator: char): TParts;

Implementation

function StringSplit(Source: string; seperator: char): TParts;
var
  Count, counter: integer;
  TArray: TParts;
  key: String;
begin
  //Get parts count.
  Count := StringParts(Source, seperator);

  for counter := 0 to Count do
  begin
     key := StringPart(Source, seperator, counter);
     if key = '' then Continue;
     TArray[counter] := key;
  end;

  //Return array
  Result := TArray;
end;

function StringParts(Source: string; seperator: char): integer;
var
  Counter, Count: integer;
begin

  Count := 0;

  if Source = '' then
    Result := 0;

  for Counter := 0 to Length(Source) do
  begin
    if Source[Counter] = seperator then
      Inc(Count);
  end;

  Result := Count;
end;

function StringPart(Source: string; seperator: char; Index: integer): string;
var
  Counter, j, iLen: integer;
  ch: char;
  Buffer, Temp: string;
begin

  //Init variables.
  Buffer := '';
  ch := #0;
  j := 0;
  Counter := 0;

  iLen := Length(Source);
  Temp := Source;

  if Temp[iLen] <> seperator then
  begin
    Temp := Temp + seperator;
  end;

  for Counter := 1 to iLen + 1 do
  begin
    //Get char.
    ch := Temp[Counter];

    if (ch <> seperator) then
    begin
      //build buffer if seperator not found.
      Buffer := Buffer + ch;
    end
    else
    begin
      //Check if we at the index.
      if (j = Index) then
      begin
        //Return string part.
        Result := Buffer;
        Exit;
      end
      else
      begin
        //INC index counter.
        Inc(j, 1);
        Buffer := '';
      end;
    end;
  end;
end;

end.
