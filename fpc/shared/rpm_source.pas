unit rpm_source;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Math;

type

  TRPMRecord = record
    Sample: Integer;
    Time: Double;
    RPM1: Integer;
    RPM2: Integer;
    RPM3: Integer;
  end;

 type
  TRPMArray = array of TRPMRecord;

  procedure LoadRPMData(const AFileName: String; var Data: TRPMArray);

implementation

procedure LoadRPMData(const AFileName: String; var Data: TRPMArray);

var
  List1, List2: TStringList;
  i, j, n: Integer;
  s: String;
  ds: char;
begin
  ds := FormatSettings.DecimalSeparator;
  List1 := TStringList.Create;
  try
    List1.LoadFromFile(AFileName);
    n := List1.Count;
    SetLength(Data, n);
    FormatSettings.DecimalSeparator := '.';
    List2 := TStringList.Create;
    try
      List2.Delimiter := ':';
      List2.StrictDelimiter := true;
      j := 0;
      for i:=0 to n-1 do begin
        List2.DelimitedText := List1[i];
        s := List1[i];
        with Data[j] do begin
          Sample := StrToInt(trim(List2[0]));
          Time := RoundTo(StrToFloat(trim(List2[2])),-3);
          RPM1 := StrToInt(trim(List2[1]));
        end;
        inc(j,1);
      end;
    finally
      List2.Free;
    end;
  finally
    FormatSettings.DecimalSeparator := ds;
    List1.Free;
  end;
end;

end.

