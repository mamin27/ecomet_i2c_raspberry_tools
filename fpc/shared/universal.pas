unit universal;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils;

function PChatToReal (in_str : PChar; limit : Integer) : Real;

implementation

uses emc2301_write;

function PChatToReal (in_str : PChar; limit : Integer) : Real;
var
  filter: String;
  test_n: Real;
const
  ALLOWED = ['0'..'9',' ','.',','];
Function Valid: Boolean;
    var
      i: Integer;
    begin
      Result := Length(filter) > 0;
      i := 1;
      while Result and (i <= Length(filter)) do
      begin
        Result := Result AND (filter[i] in ALLOWED);
        inc(i);
      end;
      if Length(filter) = 0 then Result := true;
end;
begin

  filter := StringReplace(in_str,' ','',[rfReplaceAll]);
  filter := StringReplace(filter,',','.',[rfReplaceAll]);

  if Valid then begin
    test_n := StrToFloat(filter);
    if (test_n <= limit) then
      Result := test_n
    else begin
      writeln('Number exceed ', limit);
      Result := limit;
    end;
  end
  else begin
    writeln('Wrong Input please fix');
    Result := -1;
  end;
end;

end.

