unit emc2301_write;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils,
  emc2301_pyth_util;

type
  TDict = record
    key: String;
    kval: String;
  end;

  TChip = record
    bits: String;
    bit: String;
  end;

procedure write_reg_emc (register: String; bits: Array of TChip);
procedure write_conf_reg ();
function EnumToChip (Tp: Integer; S: String) : TChip;

Implementation

uses emc2301_display;

const

  TYPE_CONF_MASK = 0;
  TYPE_CONF_DIS_TO = 1;
  TYPE_CONF_WD_EN = 2;
  TYPE_CONF_DR_EXT_CLK = 3;
  TYPE_CONF_USE_EXT_CLK = 4;
  TYPE_FAN_CONF1_EN_ALGO =5;
  TYPE_FAN_CONF1_RANGE = 6;
  TYPE_FAN_CONF1_EDGES = 7;
  TYPE_FAN_CONF1_UPDATE = 8;
  TYPE_FAN_CONF2_EN_RRC = 9;
  TYPE_FAN_CONF2_GLITCH_EN = 10;
  TYPE_FAN_CONF2_DER_OPT = 11;
  TYPE_FAN_CONF2_ERR_RNG = 12;

procedure write_reg_emc (register: String; bits: Array of TChip);
var
  Py_S: TStringList;
  content: String[100];
  register_str: String[100];
  fan_list: String;
  i: Integer;
//sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )
begin
content := 'register = ' + #39 + Trim(register) + #39 + ', bits = [';
register_str := register + '[';
i := 0;
repeat
   content := content + #39 + Trim(bits[i].bits) + #39 + ',';
   register_str := register_str + Trim(bits[i].bits) + ',';
   i := i + 1;
until  bits[i].bits = '';

content := Copy(content,0,Length(content)-1);
content := content + ']';
register_str := Copy(register_str,0,Length(register_str)-1);
register_str := register_str + ']';

fan_list := '';
if (bits[0].bit <> '') then
  begin
    content := content + ', bit = fan_list[' + #39 + Trim(bits[0].bit) + #39 + ']';
    fan_list := 'fan_list = emc2301.fan_list|';
  end;

Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.emc2301_pkg import emc2301|' +
                      'sens = emc2301.EMC2301()|' +
                      fan_list +
                      'register = ' + #39 + register_str + #39 + '|' +
                      'ret = sens.write_register(' + content + ')|' +

                      'print (":WRITE_REG:{}".format(register))|';
               //       'print (":WRITE_REG_CONF:{}".format(register)) if ret == 0 else print (":WRITE_REG_CONF_ERR:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;
end;

function EnumToChip (Tp: Integer; S: String) : TChip;
begin
  if Tp = TYPE_CONF_MASK then begin  // CONF_MASK
    if S = 'MASKED'
      then Result.bits := 'MASK';
    if S = 'UNMASKED'
      then Result.bits := 'MASK_CLR';
  end;
  if Tp = TYPE_CONF_DIS_TO then begin  // CONF_DIS_TO
    if S = 'ENABLED'
      then Result.bits := 'DIS_TO';
    if S = 'DISABLED'
      then Result.bits := 'DIS_TO_CLR';
  end;
  if Tp = TYPE_CONF_WD_EN then begin  // CONF_WD_EN
    if S = 'DISABLED'
      then Result.bits := 'WD_EN';
    if S = 'OPERATE'
      then Result.bits := 'WD_EN_CLR';
  end;
  if Tp = TYPE_CONF_DR_EXT_CLK  then begin  // CONF_DR_EXT_CLK
    if S = 'CLK_INPUT'
      then Result.bits := 'DR_EXT_CLK';
    if S = 'CLK_OUTPUT'
      then Result.bits := 'DR_EXT_CLK_CLR';
  end;
  if Tp = TYPE_CONF_USE_EXT_CLK then begin  // CONF_USE_EXT_CLK
    if S = 'INTERNAL'
      then Result.bits := 'USE_EXT_CLK';
    if S = 'EXTERNAL'
      then Result.bits := 'USE_EXT_CLK_CLR';
  end;
  if Tp = TYPE_FAN_CONF1_EN_ALGO then begin  // FAN_CONF1_EN_ALGO
    if S = 'DISABLED'
      then Result.bits := 'EN_ALGO';
    if S = 'OPERATE'
      then Result.bits := 'EN_ALGO_CLR';
  end;
//  bits = ['RANGE'], bit = fan_list['RANGE']
  if Tp = TYPE_FAN_CONF1_RANGE then begin  // FAN_CONF1_RANGE
    if S = '500>1'
      then Result.bit := 'RANGE_500_1';
    if S = '1000>2'
      then Result.bit := 'RANGE_1000_2';
    if S = '2000>4'
      then Result.bit := 'RANGE_2000_4';
    if S = '4000>8'
      then Result.bit := 'RANGE_4000_8';
    Result.bits := 'RANGE'
  end;
  if Tp = TYPE_FAN_CONF1_EDGES then begin  // FAN_CONF1_EDGES
    if S = '3>1POLE>0.5'
      then Result.bit := 'EDGES_3_1POLE_05';
    if S = '5>2POLE>1'
      then Result.bit := 'EDGES_5_2POLE_1';
    if S = '7>3POLE>1.5'
      then Result.bit := 'EDGES_7_3POLE_15';
    if S = '9>4POLE>2'
      then Result.bit := 'EDGES_9_4POLE_2';
    Result.bits := 'EDGES'
  end;
  if Tp = TYPE_FAN_CONF1_UPDATE then begin  // FAN_CONF1_UPDATE
    if S = '100ms'
      then Result.bit := 'UPDATE_100';
    if S = '200ms'
      then Result.bit := 'UPDATE_200';
    if S = '300ms'
      then Result.bit := 'UPDATE_300';
    if S = '400ms'
      then Result.bit := 'UPDATE_400';
    if S = '500ms'
      then Result.bit := 'UPDATE_500';
    if S = '800ms'
      then Result.bit := 'UPDATE_800';
    if S = '1200ms'
      then Result.bit := 'UPDATE_1200';
    if S = '1600ms'
      then Result.bit := 'UPDATE_1600';
    Result.bits := 'UPDATE'
  end;
  if Tp = TYPE_FAN_CONF2_EN_RRC then begin  // FAN_CONF2_EN_RRC
    if S = 'ENABLED'
      then Result.bits := 'EN_RRC';
    if S = 'DISABLED'
      then Result.bits := 'EN_RRC_CLR';
  end;
  if Tp = TYPE_FAN_CONF2_GLITCH_EN then begin  // FAN_CONF2_GLITCH_EN
    if S = 'ENABLED'
      then Result.bits := 'GLITCH_EN';
    if S = 'DISABLED'
      then Result.bits := 'GLITCH_EN_CLR';
  end;
  if Tp = TYPE_FAN_CONF2_DER_OPT then begin  // FAN_CONF2_DER_OPT
    if S = 'NO_DERIVATE'
      then Result.bits := 'DER_OPT_NO_DERIVATE';
    if S = 'BESIC_DERIVATE'
      then Result.bits := 'DER_OPT_BESIC_DERIVATE';
    if S = 'STEP_DERIVATE'
      then Result.bits := 'DER_OPT_STEP_DERIVATE';
    if S = 'BOTH_DERIVATE'
      then Result.bits := 'DER_OPT_BOTH_DERIVATE';
    Result.bits := 'DER_OPT';
  end;
  if Tp = TYPE_FAN_CONF2_ERR_RNG then begin  // FAN_CONF2_ERR_RNG
    if S = '0RPM'
      then Result.bits := 'ERR_RNG_0RPM';
    if S = '50RPM'
      then Result.bits := 'ERR_RNG_50RPM';
    if S = '100RPM'
      then Result.bits := 'ERR_RNG_100RPM';
    if S = '200RPM'
      then Result.bits := 'ERR_RNG_200RPM';
    Result.bits := 'ERR_RNG';
  end;
end;

procedure write_conf_reg ();
var
  conf_idx: Integer;
  conf_cmd: array [1..6] of String;
  cmd: String;
begin

  conf_idx:=0;
//  cmd := pre_write(emc.attr1.attr_val_obj.attr2.attr_chg, emc.attr1.attr_val_obj.attr2.attr_new_val);     // test change of TEMP bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     emc.attr1.attr_val_obj.attr2.attr_chg := false;
  end;

//  cmd := pre_write(emc.attr1.attr_val_obj.attr1.attr_chg, emc.attr1.attr_val_obj.attr1.attr_new_val);     // test change of HMDT bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     emc.attr1.attr_val_obj.attr1.attr_chg := false;
  end;
//  cmd := pre_write(emc.attr1.attr_val_obj.attr4.attr_chg, emc.attr1.attr_val_obj.attr4.attr_new_val);     // test change of MODE bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     emc.attr1.attr_val_obj.attr4.attr_chg := false;
  end;
//  cmd := pre_write(emc.attr1.attr_val_obj.attr5.attr_chg, emc.attr1.attr_val_obj.attr5.attr_new_val);     // test change of HEAT bit
  if cmd <> '' then begin
     conf_idx := conf_idx + 1;
     conf_cmd[conf_idx] := cmd;
     emc.attr1.attr_val_obj.attr5.attr_chg := false;
  end;

  if conf_idx <> 0 then begin
//    write_reg_emc('CONF',conf_cmd);
  end;

end;

end.

