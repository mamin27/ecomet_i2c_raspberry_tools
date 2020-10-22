unit hdc1080_pyth_util;

{$mode objfpc}{$H+}

interface

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Classes, SysUtils, ecomet_regex
  { you can add units after this };


type

  PyRecordOb_c = class(TObject)
  public
    attr_name : String[12];
    attr_val: String[15];
    attr_new_val: String[12];
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

  hdc1080Ob_c = class(TObject)
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
    attr_val: String[15];
    attr_new_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: hdc1080Ob_c;
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
    attr_val_obj: hdc1080Ob_c;
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

   hdc1080Ob = class(TObject)
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

 function StrToObj (hdc_str: String): hdc1080Ob;
 { hdc_object }

Implementation

uses hdc1080_display;

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

constructor hdc1080Ob.Init;
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

destructor hdc1080Ob.Destroy;
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

constructor hdc1080Ob_c.Init;
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

destructor hdc1080Ob_c.Destroy;
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

function StrToObj (hdc_str: String): hdc1080Ob;
var
  keys: TParts;
begin

  hdc_str := StringReplace(hdc_str,' ','',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'''',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,',',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'{',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'}',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'(',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,')',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'::',':',[rfReplaceAll, rfIgnoreCase]);
  hdc_str := StringReplace(hdc_str,'::',':',[rfReplaceAll, rfIgnoreCase]);

  //writeln('String: ' + hdc_str);
  keys := StringSplit(hdc_str,':');

  if (keys[2] = 'CONF')
   then
   begin

    idx_hdc_attr :=1;
    idx_hdc_c_attr :=1;
    idx_hdc_c :=1;

    ObI_hdc_attr[idx_hdc_attr].code_type:=keys[1];
    ObI_hdc_attr[idx_hdc_attr].attr_name:=keys[2];                      //'CONF'

    ObI_hdc_attr[idx_hdc_attr].attr_val_selector:=true;
    hdc.attr1:=ObI_hdc_attr[idx_hdc_attr];
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[3];                   //'HRES'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[4];
    Ob_hdc_c[idx_hdc_c].attr1:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[5];                   //'TRES'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[6];
    Ob_hdc_c[idx_hdc_c].attr2:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[7];                   //'BAT'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[8];
    Ob_hdc_c[idx_hdc_c].attr3:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[9];                   //'MODE'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[10];
    Ob_hdc_c[idx_hdc_c].attr4:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[11];                  //'HEAT'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[12];
    Ob_hdc_c[idx_hdc_c].attr5:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    ObI_hdc_attr[idx_hdc_attr].attr_val_obj:=Ob_hdc_c[idx_hdc_c];

    idx_hdc_attr := idx_hdc_attr +1;
    idx_hdc_c := idx_hdc_c +1;

    Ob_hdc_attr[idx_hdc_attr].attr_name:=keys[13];                      //'ID'
    Ob_hdc_attr[idx_hdc_attr].attr_val_selector:=true;
    hdc.attr2:=Ob_hdc_attr[idx_hdc_attr];
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[14];                  //'SERIAL'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[15];
    Ob_hdc_c[idx_hdc_c].attr1:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[16];                  //'MANUF'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[17];
    Ob_hdc_c[idx_hdc_c].attr2:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[18];                  //'DEVID'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[19];
    Ob_hdc_c[idx_hdc_c].attr3:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_attr[idx_hdc_attr].attr_val_obj:=Ob_hdc_c[idx_hdc_c];

   end
   else if (keys[2] = 'MEASURE')
   then
   begin

    idx_hdc_attr := idx_hdc_attr +1;
    idx_hdc_c := idx_hdc_c +1;
    idx_hdc_c_attr := idx_hdc_c_attr +1;

    ObI_hdc_attr[1].code_type:=keys[1];
    ObI_hdc_attr[1].attr_name:=keys[2];                                //'MEASURE'
    hdc.attr1:=ObI_hdc_attr[1];

    Ob_hdc_attr[idx_hdc_attr].attr_name:=keys[2];                      //'MEASURE'
    Ob_hdc_attr[idx_hdc_attr].attr_val_selector:=true;
    hdc.attr3:=Ob_hdc_attr[idx_hdc_attr];
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[3];                   //'TEMP'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[4];
    Ob_hdc_c[idx_hdc_c].attr1:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_c_attr[idx_hdc_c_attr]:= PyRecordOb_c.Init;
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:=keys[5];                   //'HUMIDITY'
    Ob_hdc_c_attr[idx_hdc_c_attr].attr_val:=keys[6];
    Ob_hdc_c[idx_hdc_c].attr2:=Ob_hdc_c_attr[idx_hdc_c_attr];
    idx_hdc_c_attr := idx_hdc_c_attr +1;
    Ob_hdc_attr[idx_hdc_attr].attr_val_obj:=Ob_hdc_c[idx_hdc_c];
   end
   else  begin
    idx_hdc_attr := idx_hdc_attr +1;
    idx_hdc_c := idx_hdc_c +1;
    idx_hdc_c_attr := idx_hdc_c_attr +1;

     ObI_hdc_attr[1].code_type:=keys[1];
     ObI_hdc_attr[1].attr_name:=keys[2];                      //WRITE
     hdc.attr1:=ObI_hdc_attr[1];

     Ob_hdc_attr[idx_hdc_attr].attr_val_selector:=false;
     hdc.attr4:=Ob_hdc_attr[idx_hdc_attr];
     Ob_hdc_c_attr[idx_hdc_c_attr].attr_name:='na';
     Ob_hdc_attr[idx_hdc_attr].attr_val_obj:=Ob_hdc_c[idx_hdc_c];
   end;

  Result := hdc;

end;

end.


