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
    attr_new_val: String[12];
    attr_chg: boolean;
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
    attr_new_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: pca6532Ob_c;
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

   PyRecordIOb = class(TObject)
   public
    code_type : String[15];
    attr_name : String[12];
    attr_val: String[12];
    attr_new_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: pca6532Ob_c;
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

   pca6532Ob = class(TObject)
   public
    attr1: PyRecordIOb;
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
    attr_new_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;
    attr_chg := false;

end;

destructor PyRecordOb.Destroy;
begin
    attr_name := '';
    attr_val := '';
    attr_new_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;
    attr_chg := false;
    inherited Destroy;
end;

constructor PyRecordIOb.Init;
begin
//    inherited Create;
    code_type := '';
    attr_name := '';
    attr_val := '';
    attr_new_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;
    attr_chg := false;

end;

destructor PyRecordIOb.Destroy;
begin
    code_type := '';
    attr_name := '';
    attr_val := '';
    attr_new_val := '';
    attr_val_selector := false;
    attr_val_obj := nil;
    attr_chg := false;
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
    attr_new_val := '';
    attr_chg := false;
end;

destructor PyRecordOb_c.Destroy;
begin
    attr_name := '';
    attr_val := '';
    attr_new_val := '';
    attr_chg := false;
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
  ObI_pca_attr: array[1..2] of PyRecordIOb;
  Ob_pca_attr: array[2..50] of PyRecordOb;
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
    if i=1 then
       ObI_pca_attr[1]:= PyRecordIOb.Init
     else
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

//  writeln('String: ' + pca_str);
  keys := StringSplit(pca_str,':');

  ObI_pca_attr[idx_pca_attr].code_type:=keys[1];
  ObI_pca_attr[idx_pca_attr].attr_name:=keys[2];                      //'MODE1'
  ObI_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr1:=ObI_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[3];                   //'ALLCALL'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[4];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[5];                   //'SUB3'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[6];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[7];                   //'SUB2'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[8];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[9];                   //'SUB1'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[10];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[11];                  //'SLEEP'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[12];
  Ob_pca_c[idx_pca_c].attr5:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  ObI_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];

  idx_pca_attr := idx_pca_attr +1;
  idx_pca_c := idx_pca_c +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[13];                      //'MODE2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr2:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[14];                  //'OUTDRV'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[15];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[16];                  //'OCH'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[17];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[18];                  //'INVRT'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[19];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[20];                  //'DMBLINK'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[21];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];

  idx_pca_attr := idx_pca_attr +1;
  idx_pca_c := idx_pca_c +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[22];                      //'PWM0'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr3:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[23];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[24];                      //'PWM1'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr4:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[25];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[26];                      //'PWM2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr5:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[27];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[28];                      //'PWM3'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr6:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[29];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[30];                      //'GRPPWM'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr7:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[31];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[32];                      //'GRPFREQ'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr8:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[33];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[34];                      //'SUBADR1'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr9:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[35];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[36];                      //'SUBADR2'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr10:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[37];
  idx_pca_attr := idx_pca_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_name:=keys[38];                      //'SUBADR3'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr11:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[39];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[40];                      //'LEDOUT'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=true;
  pca.attr12:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[41];                  //'LDR0'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[42];
  Ob_pca_c[idx_pca_c].attr1:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[43];                  //'LDR1'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[44];
  Ob_pca_c[idx_pca_c].attr2:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[45];                  //'LDR2'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[46];
  Ob_pca_c[idx_pca_c].attr3:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_c_attr[idx_pca_c_attr].attr_name:=keys[47];                  //'LDR4'
  Ob_pca_c_attr[idx_pca_c_attr].attr_val:=keys[48];
  Ob_pca_c[idx_pca_c].attr4:=Ob_pca_c_attr[idx_pca_c_attr];
  idx_pca_c_attr := idx_pca_c_attr +1;
  Ob_pca_attr[idx_pca_attr].attr_val_obj:=Ob_pca_c[idx_pca_c];
  idx_pca_attr := idx_pca_attr +1;

  Ob_pca_attr[idx_pca_attr].attr_name:=keys[49];                      //'ALLCALLADR'
  Ob_pca_attr[idx_pca_attr].attr_val_selector:=false;
  pca.attr13:=Ob_pca_attr[idx_pca_attr];
  Ob_pca_attr[idx_pca_attr].attr_val:=keys[50];

  Result := pca;

end;

end.

