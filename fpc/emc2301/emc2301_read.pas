unit emc2301_read;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  emc2301_pyth_util, emc2301_display;

procedure read_output_emc (emc: emc2301Ob);
procedure read_emc ();
procedure read_measure ();
procedure self_test ();
{procedure read_measure_emc  (emc: emc2301Ob); }
function EnumToInt (Tp: Integer; S: String) : Integer;
function EnumToInt_MODE (S: String) : Integer;
function EnumToInt_HEAT (S: String) : Integer;
function IntToEnum (Tp: Integer; S: Integer) : String;
function IntToEnum_MODE (S: Integer) : String;
function IntToEnum_HEAT (S: Integer) : String;

Implementation

const

  TYPE_MASK = 0;
  TYPE_ENABLE = 1;
  TYPE_OPER = 2;
  TYPE_DR_CLK = 3;
  TYPE_USE_CLK = 4;
  TYPE_RANGE = 5;
  TYPE_EDGE = 6;
  TYPE_UPDATE = 7;
  TYPE_DER_OPT = 8;
  TYPE_ERR_RNG = 9;
  TYPE_GAIN = 10;

function EnumToInt (Tp: Integer; S: String) : Integer;
begin
  if Tp = 0 then begin  // MASK
    if S = 'MASKED'
      then Result := 0;
    if S = 'UNMASKED'
      then Result := 1;
  end;
  if Tp = 1 then begin  // ENABLE
    if S = 'ENABLED'
      then Result := 0;
    if S = 'DISABLED'
      then Result := 1;
  end;
  if Tp = 2 then begin  // OPER
    if S = 'DISABLED'
      then Result := 0;
    if S = 'OPERATE'
      then Result := 1;
  end;
  if Tp = 3 then begin  // DR_CLK
    if S = 'CLK_INPUT'
      then Result := 0;
    if S = 'CLK_OUTPUT'
      then Result := 1;
  end;
  if Tp = 4 then begin  // USE_CLK
    if S = 'INTERNAL'
      then Result := 0;
    if S = 'EXTERNAL'
      then Result := 1;
  end;
  if Tp = 5 then begin  // RANGE
    if S = '500>1'
      then Result := 0;
    if S = '1000>2'
      then Result := 32;
    if S = '2000>4'
      then Result := 64;
    if S = '4000>8'
      then Result := 96;
  end;
  if Tp = 6 then begin  // EDGE
    if S = '3>1POLE>0.5'
      then Result := 0;
    if S = '5>2POLE>1'
      then Result := 8;
    if S = '7>3POLE>1.5'
      then Result := 16;
    if S = '9>4POLE>2'
      then Result := 24;
  end;
  if Tp = 7 then begin  // UPDATE
    if S = '100ms'
      then Result := 0;
    if S = '200ms'
      then Result := 1;
    if S = '300ms'
      then Result := 2;
    if S = '400ms'
      then Result := 3;
    if S = '500ms'
      then Result := 4;
    if S = '800ms'
      then Result := 5;
    if S = '1200ms'
      then Result := 6;
    if S = '1600ms'
      then Result := 7;
  end;
  if Tp = 8 then begin  // DER_OPT
    if S = 'NO_DERIVATE'
      then Result := 0;
    if S = 'BASIC_DERIVATE'
      then Result := 8;
    if S = 'STEP_DERIVATE'
      then Result := 16;
    if S = 'BOTH_DERIVATE'
      then Result := 24;
  end;
  if Tp = 9 then begin  // ERR_RNG
    if S = '0RPM'
      then Result := 0;
    if S = '50RPM'
      then Result := 2;
    if S = '100RPM'
      then Result := 4;
    if S = '200RPM'
      then Result := 6;
  end;
  if Tp = 10 then begin  // ERR_RNG
    if S = '1x'
      then Result := 0;
    if S = '2x'
      then Result := 1;
    if S = '4x'
      then Result := 2;
    if S = '8x'
      then Result := 3;
  end;
end;

function IntToEnum (Tp: Integer; S: Integer) : String;
begin
  if Tp = 1 then begin  // TEMP
    if S = 0
      then Result := 'TRES_RES2';
    if S = 1
      then Result := 'TRES_RES1';
  end;
  if Tp = 0 then begin  // HMDT
    if S = 0
      then Result := 'HRES_RES3';
    if S = 1
      then Result := 'HRES_RES2';
    if S = 2
      then Result := 'HRES_RES1';
  end;
end;

function EnumToInt_MODE (S: String) : Integer;
begin
    if S = 'BOTH'
      then Result := 0;
    if S = 'ONLY'
      then Result := 1;
end;

function IntToEnum_MODE (S: Integer) : String;
begin
    if S = 0
      then Result := 'MODE_BOTH';
    if S = 1
      then Result := 'MODE_ONLY';
end;

function EnumToInt_HEAT (S: String) : Integer;
begin
    if S = 'DISABLE'
      then Result := 0;
    if S = 'ENABLE'
      then Result := 1;
end;

function IntToEnum_HEAT (S: Integer) : String;
begin
    if S = 0
      then Result := 'HEAT_DISABLE';
    if S = 1
      then Result := 'HEAT_ENABLE';
end;

procedure read_emc ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.emc2301_pkg import emc2301|' +
                      'register = emc2301.conf_register_list()|' +
                      'if register != "" :|' +
                      '    print (":READ_emc:{}".format(register))|' +
                      'else :|' +
                      '    print(":READ_emc_ERR:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_measure ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.emc2301_pkg import emc2301|' +
                      'from i2c_pkg.emc2301_pkg import fan_type|' +
                      'register = emc2301.conf_register_list()|' +
                      'if register != "" :|' +
                      '    print (":READ_MEASURE:{}".format(register))|' +
                      'else :|' +
                      '    print (":READ_MEASURE_ERR:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;
end;

procedure self_test ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.emc2301_pkg import emc2301|' +
                      'from i2c_pkg.emc2301_pkg import fan_type|' +
                      'sens = emc2301.EMC2301()|' +
                      'ret = sens.self_test()|' +
                      'if ret == 0 :|' +
                      '    print(":TEST_PASSED:")|' +
                      'else :|' +
                      '    print(":MISSING_CHIP:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;
end;

procedure read_output_emc (emc: emc2301Ob);
begin

                                                                                                     //CONF REG
  Form_emc2301.CB_CONF_MASK.ItemIndex := EnumToInt(TYPE_MASK,emc.attr1.attr_val_obj.attr1.attr_val);     //MASK 0-MASKED, 1-UNMASKED
  Form_emc2301.CB_CONF_DIS_TO.ItemIndex := EnumToInt(TYPE_ENABLE,emc.attr1.attr_val_obj.attr2.attr_val);     //DIS_TO 0-ENABLED, 1-DISABLED
  Form_emc2301.CB_CONF_WD_EN.ItemIndex := EnumToInt(TYPE_OPER,emc.attr1.attr_val_obj.attr3.attr_val);     //WD_EN 0-DISABLED, 1-OPERATE
  Form_emc2301.CB_CONF_DR_EXT_CLK.ItemIndex := EnumToInt(TYPE_DR_CLK,emc.attr1.attr_val_obj.attr4.attr_val);     //DR_EXT_CLK 0-CLK_INPUT, 1-CLK_OUTPUT
  Form_emc2301.CB_CONF_USE_EXT_CLK.ItemIndex := EnumToInt(TYPE_USE_CLK,emc.attr1.attr_val_obj.attr5.attr_val);     //USE_EXT_CLK 0-INTERNAL, 1-EXTERNAL
  Form_emc2301.CB_CONF_EN_ALGO.ItemIndex := EnumToInt(TYPE_ENABLE,emc.attr1.attr_val_obj.attr6.attr_val);     //EN_ALGE 0-MASKED, 1-UNMASKED
  Form_emc2301.CB_CONF_RANGE.ItemIndex := EnumToInt(TYPE_RANGE,emc.attr1.attr_val_obj.attr7.attr_val);     //RANGE
  Form_emc2301.CB_CONF_EDGES.ItemIndex := EnumToInt(TYPE_EDGE,emc.attr1.attr_val_obj.attr8.attr_val);     //EDGE
  Form_emc2301.CB_CONF_UPDATE.ItemIndex := EnumToInt(TYPE_UPDATE,emc.attr1.attr_val_obj.attr9.attr_val);     //UPDATE
  Form_emc2301.CB_CONF_EN_RRC.ItemIndex := EnumToInt(TYPE_ENABLE,emc.attr1.attr_val_obj.attr10.attr_val);     //EN_RRC 0-ENABLED, 1-DISABLED
  Form_emc2301.CB_CONF_GLITCH_EN.ItemIndex := EnumToInt(TYPE_ENABLE,emc.attr1.attr_val_obj.attr11.attr_val);     //GLITCH_EN 0-ENABLED, 1-DISABLED
  Form_emc2301.CB_CONF_DER_OPT.ItemIndex := EnumToInt(TYPE_DER_OPT,emc.attr1.attr_val_obj.attr12.attr_val);     //DER_OPT
  Form_emc2301.CB_CONF_ERR_RNG.ItemIndex := EnumToInt(TYPE_ERR_RNG,emc.attr1.attr_val_obj.attr13.attr_val);     //ERR_RNG
  Form_emc2301.CB_CONF_GAIND.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr14.attr_val);     //GAIND
  Form_emc2301.CB_CONF_GAINI.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr15.attr_val);     //GAINI
  Form_emc2301.CB_CONF_GAINP.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr16.attr_val);     //GAINP
  Form_emc2301.CB_CONF_MASK.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_DIS_TO.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_WD_EN.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_DR_EXT_CLK.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_USE_EXT_CLK.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_EN_ALGO.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_RANGE.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_EDGES.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_UPDATE.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_EN_RRC.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_GLITCH_EN.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_DER_OPT.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_ERR_RNG.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_GAIND.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_GAINI.Style := csOwnerDrawVariable;
  Form_emc2301.CB_CONF_GAINP.Style := csOwnerDrawVariable;

//  Form_emc2301.Edit_serial.Text:= emc.attr2.attr_val_obj.attr1.attr_val;  //SERIAL
//  Form_emc2301.Edit_serial.Alignment:=taRightJustify;
//  Form_emc2301.Edit_manuf.Text:= emc.attr2.attr_val_obj.attr2.attr_val;  //MANUFACTURER
//  Form_emc2301.Edit_manuf.Alignment:=taRightJustify;
//  Form_emc2301.Edit_devid.Text:= emc.attr2.attr_val_obj.attr3.attr_val;  //DEVICE ID
//  Form_emc2301.Edit_devid.Alignment:=taRightJustify;

end;
{
procedure  read_measure_emc  (emc: emc2301Ob);
var
  i: Real;
  const s: string = #$E2#$84#$83; // degree Celsius

begin
  i := StrToFloat(emc.attr3.attr_val_obj.attr1.attr_val);
  Form_emc2301.Edit_temp.Text:= FloatToStr(RoundTo(i,-2)) + s;  //TEMPERATURE
  Form_emc2301.Edit_temp.Alignment:=taRightJustify;
  i := StrToFloat(emc.attr3.attr_val_obj.attr2.attr_val);
  Form_emc2301.Edit_hmdt.Text:= FloatToStr(RoundTo(i,-2)) + '%';  //HUMIDITY
  Form_emc2301.Edit_hmdt.Alignment:=taRightJustify;

end;
}
end.

