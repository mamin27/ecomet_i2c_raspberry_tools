unit emc2301_pyth_util;

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
    attr_val: String[100];
    attr_new_val: String[12];
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

  emc2301Ob_c = class(TObject)
   public
    attr1: PyRecordOb_c;
    attr2: PyRecordOb_c;
    attr3: PyRecordOb_c;
    attr4: PyRecordOb_c;
    attr5: PyRecordOb_c;
    attr6: PyRecordOb_c;
    attr7: PyRecordOb_c;
    attr8: PyRecordOb_c;
    attr9: PyRecordOb_c;
    attr10: PyRecordOb_c;
    attr11: PyRecordOb_c;
    attr12: PyRecordOb_c;
    attr13: PyRecordOb_c;
    attr14: PyRecordOb_c;
    attr15: PyRecordOb_c;
    attr16: PyRecordOb_c;
    constructor Init;
    destructor Destroy; override;
   end;

  PyRecordOb = class(TObject)
  public
    attr_name : String[12];
    attr_val: String[15];
    attr_new_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: emc2301Ob_c;
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

   PyRecordIOb = class(TObject)
   public
    code_type : String[15];
    attr_name : String[60];
    attr_val: String[15];
    attr_new_val: String[12];
    attr_val_selector: boolean;
    attr_val_obj: emc2301Ob_c;
    attr_chg: boolean;
    constructor Init;
    destructor Destroy; override;
   end;

   emc2301Ob = class(TObject)
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
    constructor Init;
    destructor Destroy; override;
   end;

 function StrToObj (emc_str: String): emc2301Ob;
 { emc_object }

Implementation

uses emc2301_display;

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

constructor emc2301Ob.Init;
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
end;

destructor emc2301Ob.Destroy;
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

constructor emc2301Ob_c.Init;
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
    attr9 := nil;
    attr10 := nil;
    attr11 := nil;
    attr12 := nil;
    attr13 := nil;
    attr14 := nil;
    attr15 := nil;
    attr16 := nil;
end;

destructor emc2301Ob_c.Destroy;
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
    attr14 := nil;
    attr15 := nil;
    attr16 := nil;
    inherited Destroy;
end;

function StrToObj (emc_str: String): emc2301Ob;
var
  keys: TParts;
begin

  emc_str := StringReplace(emc_str,' ','',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'''',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,',',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'{',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'}',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'(',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,')',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'::',':',[rfReplaceAll, rfIgnoreCase]);
  emc_str := StringReplace(emc_str,'::',':',[rfReplaceAll, rfIgnoreCase]);

//  writeln('String: ' + emc_str);
  keys := StringSplit(emc_str,':');

  if (keys[2] = 'CONF')
   then
   begin

    idx_emc_attr :=1;
    idx_emc_c_attr :=1;
    idx_emc_c :=1;

    ObI_emc_attr[idx_emc_attr].code_type:=keys[1];
    ObI_emc_attr[idx_emc_attr].attr_name:=keys[2];                      //'CONF'

    ObI_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr1:=ObI_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[3];                   //'MASK'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[4];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[5];                   //'DIS_TO'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[6];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[7];                   //'WD_EN'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[8];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[9];                   //'DR_EXT_CLK'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[10];
    Ob_emc_c[idx_emc_c].attr4:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[11];                  //'USE_EXT_CLK'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[12];
    Ob_emc_c[idx_emc_c].attr5:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[13];                  //'EN_ALGO'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[14];
    Ob_emc_c[idx_emc_c].attr6:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[15];                  //'RANGE'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[16];
    Ob_emc_c[idx_emc_c].attr7:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[17];                  //'EDGES'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[18];
    Ob_emc_c[idx_emc_c].attr8:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[19];                  //'UPDATE'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[20];
    Ob_emc_c[idx_emc_c].attr9:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[21];                  //'EN_RRC'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[22];
    Ob_emc_c[idx_emc_c].attr10:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[23];                  //'GLITCH_EN'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[24];
    Ob_emc_c[idx_emc_c].attr11:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[25];                  //'DER_OPT'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[26];
    Ob_emc_c[idx_emc_c].attr12:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[27];                  //'ERR_RNG'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[28];
    Ob_emc_c[idx_emc_c].attr13:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[29];                  //'GAIND'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[30];
    Ob_emc_c[idx_emc_c].attr14:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[31];                  //'GAINI'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[32];
    Ob_emc_c[idx_emc_c].attr15:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[33];                  //'GAINP'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[34];
    Ob_emc_c[idx_emc_c].attr16:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    ObI_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[35];                      //'FAN_STAT'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr2:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[36];                  //'WATCH'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[37];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[38];                  //'DRIVE_FAIL'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[39];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[40];                  //'FAN_SPIN'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[41];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[42];                  //'FAN_STALL'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[43];
    Ob_emc_c[idx_emc_c].attr4:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[44];                  //'FAN_INT'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[45];
    Ob_emc_c[idx_emc_c].attr5:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[46];                  //'FAN_SETTING'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[47];
    Ob_emc_c[idx_emc_c].attr6:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[48];                      //'SPIN'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr3:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[49];                  //'DRIVE_FAIL_CNT'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[50];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[51];                  //'NOKICK'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[52];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[53];                  //'SPIN_LVL'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[54];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[55];                  //'SPINUP_TIME'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[56];
    Ob_emc_c[idx_emc_c].attr4:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[57];                  //'FAN_MAX_STEP'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[58];
    Ob_emc_c[idx_emc_c].attr5:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[59];                  //'FAN_MIN_DRIVE'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[60];
    Ob_emc_c[idx_emc_c].attr6:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[61];                      //'PWM'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr4:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[62];                  //'PWM_POLARITY'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[63];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[64];                  //'PWM_OUTPUT'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[65];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[66];                  //'PWM_BASE'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[67];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[68];                  //'PWM_DIVIDE'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[69];
    Ob_emc_c[idx_emc_c].attr4:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[70];                      //'TACH'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr5:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[71];                  //'TACH_COUNT'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[72];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[73];                  //'FAN_FAIL_BAND'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[74];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[75];                  //'TACH_TARGET'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[76];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[77];                  //'TACH_READ'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[78];
    Ob_emc_c[idx_emc_c].attr4:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[79];                      //'ID'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr6:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[80];                  //'PRODUCT_ID'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[81];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[82];                  //'MANUF_ID'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[83];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[84];                  //'REVISION_ID'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[85];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;

    Ob_emc_attr[idx_emc_attr].attr_name:=keys[86];                      //'SOFTWARE_LOCK'
    Ob_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr7:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:='LOCK';
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[87];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

   end
   else if (keys[2] = 'SPEED')
   then
   begin

    idx_emc_attr := idx_emc_attr + 1;
    idx_emc_c := idx_emc_c + 1;
    idx_emc_c_attr := idx_emc_c_attr + 1;

    ObI_emc_attr[1].code_type:=keys[1];                      //READ_speed
    ObI_emc_attr[1].attr_name:=keys[2];                      //'SPEED'
    emc.attr1:=ObI_emc_attr[1];

    ObI_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr8:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:=keys[3];                   //'RPM'
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[4];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

   end
   else if (keys[2] = 'WRITE')
   then
   begin

    idx_emc_attr := idx_emc_attr + 1;
    idx_emc_c := idx_emc_c + 1;
    idx_emc_c_attr := 1;

    ObI_emc_attr[1].code_type:=keys[1];                      //WRITE_REG
    ObI_emc_attr[1].attr_name:=keys[2];                      //'WRITE'
    emc.attr1:=ObI_emc_attr[1];

    ObI_emc_attr[idx_emc_attr].attr_val_selector:=true;
    emc.attr9:=Ob_emc_attr[idx_emc_attr];
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:='REGISTER';                   //REGISTER
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[3];
    Ob_emc_c[idx_emc_c].attr1:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:='CONTENT';                    //CONTENT
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[4];
    Ob_emc_c[idx_emc_c].attr2:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_c_attr[idx_emc_c_attr].attr_name:='RET';                         //RET
    Ob_emc_c_attr[idx_emc_c_attr].attr_val:=keys[5];
    Ob_emc_c[idx_emc_c].attr3:=Ob_emc_c_attr[idx_emc_c_attr];
    idx_emc_c_attr := idx_emc_c_attr +1;
    Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];

   end
   else  begin
    idx_emc_attr := idx_emc_attr +1;
    idx_emc_c := idx_emc_c +1;
    idx_emc_c_attr := idx_emc_c_attr +1;

     ObI_emc_attr[1].code_type:=keys[1];                      //TEST_PASSED or MISSING_CHIP
     ObI_emc_attr[1].attr_name:=keys[2];                      //
     emc.attr1:=ObI_emc_attr[1];

     Ob_emc_attr[idx_emc_attr].attr_val_selector:=false;
     emc.attr9:=Ob_emc_attr[idx_emc_attr];
     Ob_emc_c_attr[idx_emc_c_attr].attr_name:='na';
     Ob_emc_attr[idx_emc_attr].attr_val_obj:=Ob_emc_c[idx_emc_c];
   end;

  Result := emc;

end;

end.


