unit pca_pyth_util;

{$mode objfpc}{$H+}

interface

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Classes, SysUtils, CustApp, pca_regex
  { you can add units after this };


type

  PyRecordOb_c = class(TObject)
  public
    attr_name : String[12];
    attr_val: String[12];
    constructor Init;
    destructor Destroy; override;
   end;

  pca6532Ob_c = class(TObject)
   public
    attr1: PyRecordOb_c;
    attr2: PyRecordOb_c;
    attr3: PyRecordOb_c;
    attr4: PyRecordOb_c;
    attr5: PyRecordOb_c;
    attr6: PyRecordOb_c;
    attr7: PyRecordOb_c;
    attr8: PyRecordOb_c;
    constructor Init;
    destructor Destroy; override;
   end;

  PyRecordOb = class(TObject)
  public
    attr_name : String[12];
    attr_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: pca6532Ob_c;
    constructor Init;
    destructor Destroy; override;
   end;

   pca6532Ob = class(TObject)
   public
    attr1: PyRecordOb;
    attr2: PyRecordOb;
    attr3: PyRecordOb;
    attr4: PyRecordOb;
    attr5: PyRecordOb;
    attr6: PyRecordOb;
    attr7: PyRecordOb;
    attr8: PyRecordOb;
    attr9: PyRecordOb;
    attr10: PyRecordOb;
    attr11: PyRecordOb;
    attr12: PyRecordOb;
    attr13: PyRecordOb;
    constructor Init;
    destructor Destroy; override;
   end;

 function StrToObj (pca_str: String): pca6532Ob;
 { pca_object }

Implementation

//  function StrToObj (S: String): PyRecordOb_c;

constructor PyRecordOb.Init;
begin
//    inherited Create;
    attr_name := '';
    attr_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;

end;

destructor PyRecordOb.Destroy;
begin
    attr_name := '';
    attr_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;
    inherited Destroy;
end;

constructor pca6532Ob.Init;
begin
  //  inherited Create;
    attr1 := nil;
    attr2 := nil;
    attr3 := nil;
    attr4 := nil;
    attr5 := nil;
    attr6 := nil;
    attr7 := nil;
    attr8 := nil;
    attr9 := nil;
    attr10 := nil;
    attr11 := nil;
    attr12 := nil;
    attr13 := nil;
end;

destructor pca6532Ob.Destroy;
begin
    attr1 := nil;
    attr2 := nil;
    attr3 := nil;
    attr4 := nil;
    attr5 := nil;
    attr6 := nil;
    attr7 := nil;
    attr8 := nil;
    attr9 := nil;
    attr10 := nil;
    attr11 := nil;
    attr12 := nil;
    attr13 := nil;
    inherited Destroy;
end;

constructor PyRecordOb_c.Init;
begin
//    inherited Create;
    attr_name := '';
    attr_val := '';
end;

destructor PyRecordOb_c.Destroy;
begin
    attr_name := '';
    attr_val := '';
    inherited Destroy;
end;

constructor pca6532Ob_c.Init;
begin
//    inherited Create;
    attr1 := nil;
    attr2 := nil;
    attr3 := nil;
    attr4 := nil;
    attr5 := nil;
    attr6 := nil;
    attr7 := nil;
    attr8 := nil;
end;

destructor pca6532Ob_c.Destroy;
begin
    attr1 := nil;
    attr2 := nil;
    attr3 := nil;
    attr4 := nil;
    attr5 := nil;
    attr6 := nil;
    attr7 := nil;
    attr8 := nil;
    inherited Destroy;
end;

function StrToObj (pca_str: String): pca6532Ob;
var
  i: Integer;
  pca: pca6532Ob;
  // pca_attr: PyRecordOb;
  // pca_c:  pca6532Ob_c;
  // pca_c_attr: PyRecordOb_c;
  Ob_pca_c_attr: array[1..50] of PyRecordOb_c;
  Ob_pca_attr: array[1..50] of PyRecordOb;
  Ob_pca_c: array[1..50] of pca6532Ob_c;
  idx_pca_attr,idx_pca_c_attr,idx_pca_c: integer;
  keys: TParts;
  // idx: Integer;
begin

  pca := pca6532Ob.Init;
 // pca_c := pca6532Ob_c.Init;
  for i in [1..50] do
    begin
    Ob_pca_c_attr[i]:= PyRecordOb_c.Init;
    Ob_pca_attr[i]:= PyRecordOb.Init;
    Ob_pca_c[i]:= pca6532Ob_c.Init;
    end;

  idx_pca_attr :=1;
  idx_pca_c_attr :=1;
  idx_pca_c :=1;

  pca_str := StringReplace(pca_str,' ','',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,'''',':',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,',',':',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,'{',':',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,'}',':',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,'::',':',[rfReplaceAll, rfIgnoreCase]);
  pca_str := StringReplace(pca_str,'::',':',[rfReplaceAll, rfIgnoreCase]);

  keys := StringSplit(pca_str,':');

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[1];                       //'MODE1'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr1:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[2];                   //'ALLCALL'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[3];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[4];                   //'SUB3'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[5];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[6];                   //'SUB2'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[7];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[8];                   //'SUB1'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[9];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[10];                  //'SLEEP'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[11];
  Ob_pca_c[idx_pca_c].attr5:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];

  idx_pca_attr := idx_pca_attr +1;
  idx_pca_c := idx_pca_c +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[12];                      //'MODE2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr2:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[13];                  //'OUTDRV'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[14];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[15];                  //'OCH'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[16];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[17];                  //'INVRT'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[18];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[19];                  //'DMBLINK'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[20];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];

  idx_pca_attr := idx_pca_attr +1;
  idx_pca_c := idx_pca_c +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[21];                      //'PWM0'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr3:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[22];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[23];                      //'PWM1'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr4:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[24];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[25];                      //'PWM2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr5:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[26];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[27];                      //'PWM3'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr6:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[28];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[29];                      //'GRPPWM'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr7:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[30];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[31];                      //'GRPFREQ'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr8:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[32];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[33];                      //'SUBADR1'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr9:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[34];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[35];                      //'SUBADR2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr10:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[36];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[37];                      //'SUBADR3'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr11:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[38];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[39];                      //'LEDOUT'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr12:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[40];                  //'LDR0'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[41];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[42];                  //'LDR1'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[43];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[44];                  //'LDR2'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[45];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[46];                  //'LDR4'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[47];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[48];                      //'ALLCALLADR'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr13:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[49];

  Result := pca;

end;

end.

