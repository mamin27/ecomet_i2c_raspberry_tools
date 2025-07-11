unit emc2301_write;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils;

type
  TDict = record
    key: String;
    kval: String;
  end;

  TChip = record
    rbyte: String;
    rbit: String;
  end;

procedure write_reg_emc (register: String; subr: Array of TChip);
procedure write_reg_emc_value (register: String; value: Integer);
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
  TYPE_GAIN_GAIND = 13;
  TYPE_GAIN_GAINI = 14;
  TYPE_GAIN_GAINP = 15;
  TYPE_FAN_SPIN_UP_TIME =  16;
  TYPE_FAN_SPIN_UP_LVL = 17;
  TYPE_FAN_SPIN_UP_NOKICK = 18;
  TYPE_FAN_SPIN_UP_DRIVE_FAIL = 19;

  TYPE_FAN_STAT_INT = 20;
  TYPE_FAN_PWM_POLARITY = 21;
  TYPE_FAN_PWM_OUTPUT = 22;
  TYPE_FAN_PWM_BASE = 23;

  TYPE_LOCKED = 24;


procedure write_reg_emc (register: String; subr: Array of TChip);
var
  Py_S: TStringList;
  content: String[100];
  register_str: String[100];
  content_str: String[100];
  fan_list: String;
  i: Integer;
//sens.write_register(register = 'FAN_CONF1', bits = ['RANGE'], bit = fan_list['RANGE'] )
begin
content := 'register = ' + #39 + Trim(register) + #39 + ', bits = [';
register_str := register + '[';
i := 0;
repeat
   content := content + #39 + Trim(subr[i].rbyte) + #39 + ',';
   register_str := register_str + Trim(subr[i].rbyte) + ',';
   i := i + 1;
until  subr[i].rbyte = '';

content := Copy(content,0,Length(content)-1);
content := content + ']';
register_str := Copy(register_str,0,Length(register_str)-1);
register_str := register_str + ']';

fan_list := '';
if (subr[0].rbit <> '') then
  begin
    content := content + ', bit = fan_list[' + #39 + Trim(subr[0].rbit) + #39 + ']';
    fan_list := 'fan_list = emc2301.fan_list|';
  end;

writeln(content);
content_str := StringReplace(content,'''','',[rfReplaceAll, rfIgnoreCase]);
content_str := StringReplace(content_str,',','-',[rfReplaceAll, rfIgnoreCase]);

Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  ecomet_i2c_sensors.emc2301 import emc2301|' +
                      'sens = emc2301.EMC2301()|' +
                      fan_list +
                      'content = ' + #34 + content_str + #34 + '|' +
                      'register = ' + #39 + register_str + #39 + '|' +
                      'ret = sens.write_register(' + content + ')|' +

                      'print (":WRITE_REG:WRITE:{}:{}:{}".format(register,content,ret))|';
               //       'print (":WRITE_REG_CONF:{}".format(register)) if ret == 0 else print (":WRITE_REG_CONF_ERR:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;
end;

procedure write_reg_emc_value (register: String; value: Integer);
var
  Py_S: TStringList;
  content: String[100];
  content_str: String[100];

//sens.write_register(register = 'FAN_MAX_STEP', value = 20 )
begin

content := 'register = ' + #39 + Trim(register) + #39 + ', value = ' + IntToStr(value);
content_str := Trim(register) + '[value = ' + IntToStr(value) + ']';

writeln(content);

Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  ecomet_i2c_sensors.emc2301 import emc2301|' +
                      'sens = emc2301.EMC2301()|' +
                      'content = ' + #34 + content_str + #34 + '|' +
                      'register = ' + #39 + register + #39 + '|' +
                      'ret = sens.write_register(' + content + ')|' +

                      'print (":WRITE_REG:WRITE:{}:{}:{}".format(register,content,ret))|';
               //       'print (":WRITE_REG_CONF:{}".format(register)) if ret == 0 else print (":WRITE_REG_CONF_ERR:")|';

Form_emc2301.PythonEngine_emc2301.ExecStrings(Py_S);
Py_S.Free;


end;

function EnumToChip (Tp: Integer; S: String) : TChip;
begin
  if Tp = TYPE_CONF_MASK then begin  // CONF_MASK
    if S = 'MASKED'
      then Result.rbyte := 'MASK';
    if S = 'UNMASKED'
      then Result.rbyte := 'MASK_CLR';
  end;
  if Tp = TYPE_CONF_DIS_TO then begin  // CONF_DIS_TO
    if S = 'ENABLED'
      then Result.rbyte := 'DIS_TO';
    if S = 'DISABLED'
      then Result.rbyte := 'DIS_TO_CLR';
  end;
  if Tp = TYPE_CONF_WD_EN then begin  // CONF_WD_EN
    if S = 'DISABLED'
      then Result.rbyte := 'WD_EN';
    if S = 'OPERATE'
      then Result.rbyte := 'WD_EN_CLR';
  end;
  if Tp = TYPE_CONF_DR_EXT_CLK  then begin  // CONF_DR_EXT_CLK
    if S = 'CLK_INPUT'
      then Result.rbyte := 'DR_EXT_CLK';
    if S = 'CLK_OUTPUT'
      then Result.rbyte := 'DR_EXT_CLK_CLR';
  end;
  if Tp = TYPE_CONF_USE_EXT_CLK then begin  // CONF_USE_EXT_CLK
    if S = 'INTERNAL'
      then Result.rbyte := 'USE_EXT_CLK';
    if S = 'EXTERNAL'
      then Result.rbyte := 'USE_EXT_CLK_CLR';
  end;
  if Tp = TYPE_FAN_CONF1_EN_ALGO then begin  // FAN_CONF1_EN_ALGO
    if S = 'DISABLED'
      then Result.rbyte := 'EN_ALGO_CLR';
    if S = 'ENABLED'
      then Result.rbyte := 'EN_ALGO';
  end;
//  byte = ['RANGE'], bit = fan_list['RANGE']
  if Tp = TYPE_FAN_CONF1_RANGE then begin  // FAN_CONF1_RANGE
    if S = '500>1'
      then Result.rbit := 'RANGE_500_1';
    if S = '1000>2'
      then Result.rbit := 'RANGE_1000_2';
    if S = '2000>4'
      then Result.rbit := 'RANGE_2000_4';
    if S = '4000>8'
      then Result.rbit := 'RANGE_4000_8';
    Result.rbyte := 'RANGE'
  end;
  if Tp = TYPE_FAN_CONF1_EDGES then begin  // FAN_CONF1_EDGES
    if S = '3>1POLE>0.5'
      then Result.rbit := 'EDGES_3_1POLE_05';
    if S = '5>2POLE>1'
      then Result.rbit := 'EDGES_5_2POLE_1';
    if S = '7>3POLE>1.5'
      then Result.rbit := 'EDGES_7_3POLE_15';
    if S = '9>4POLE>2'
      then Result.rbit := 'EDGES_9_4POLE_2';
    Result.rbyte := 'EDGES'
  end;
  if Tp = TYPE_FAN_CONF1_UPDATE then begin  // FAN_CONF1_UPDATE
    if S = '100ms'
      then Result.rbit := 'UPDATE_100';
    if S = '200ms'
      then Result.rbit := 'UPDATE_200';
    if S = '300ms'
      then Result.rbit := 'UPDATE_300';
    if S = '400ms'
      then Result.rbit := 'UPDATE_400';
    if S = '500ms'
      then Result.rbit := 'UPDATE_500';
    if S = '800ms'
      then Result.rbit := 'UPDATE_800';
    if S = '1200ms'
      then Result.rbit := 'UPDATE_1200';
    if S = '1600ms'
      then Result.rbit := 'UPDATE_1600';
    Result.rbyte := 'UPDATE'
  end;
  if Tp = TYPE_FAN_CONF2_EN_RRC then begin  // FAN_CONF2_EN_RRC
    if S = 'ENABLED'
      then Result.rbyte := 'EN_RRC';
    if S = 'DISABLED'
      then Result.rbyte := 'EN_RRC_CLR';
  end;
  if Tp = TYPE_FAN_CONF2_GLITCH_EN then begin  // FAN_CONF2_GLITCH_EN
    if S = 'ENABLED'
      then Result.rbyte := 'GLITCH_EN';
    if S = 'DISABLED'
      then Result.rbyte := 'GLITCH_EN_CLR';
  end;
  if Tp = TYPE_FAN_CONF2_DER_OPT then begin  // FAN_CONF2_DER_OPT
    if S = 'NO_DERIVATE'
      then Result.rbit := 'DER_OPT_NO_DERIVATE';
    if S = 'BASIC_DERIVATE'
      then Result.rbit := 'DER_OPT_BASIC_DERIVATE';
    if S = 'STEP_DERIVATE'
      then Result.rbit := 'DER_OPT_STEP_DERIVATE';
    if S = 'BOTH_DERIVATE'
      then Result.rbit := 'DER_OPT_BOTH_DERIVATE';
    Result.rbyte := 'DER_OPT';
  end;
  if Tp = TYPE_FAN_CONF2_ERR_RNG then begin  // FAN_CONF2_ERR_RNG
    if S = '0RPM'
      then Result.rbit := 'ERR_RNG_0RPM';
    if S = '50RPM'
      then Result.rbit := 'ERR_RNG_50RPM';
    if S = '100RPM'
      then Result.rbit := 'ERR_RNG_100RPM';
    if S = '200RPM'
      then Result.rbit := 'ERR_RNG_200RPM';
    Result.rbyte := 'ERR_RNG';
  end;
  if Tp = TYPE_GAIN_GAIND then begin  // GAIND
    if S = '1x'
      then Result.rbit := 'GAIN_GAIND_1x';
    if S = '2x'
      then Result.rbit := 'GAIN_GAIND_2x';
    if S = '4x'
      then Result.rbit := 'GAIN_GAIND_4x';
    if S = '8x'
      then Result.rbit := 'GAIN_GAIND_8x';
    Result.rbyte := 'GAIND';
  end;
  if Tp = TYPE_GAIN_GAINI then begin  // GAINI
    if S = '1x'
      then Result.rbit := 'GAIN_GAINI_1x';
    if S = '2x'
      then Result.rbit := 'GAIN_GAINI_2x';
    if S = '4x'
      then Result.rbit := 'GAIN_GAINI_4x';
    if S = '8x'
      then Result.rbit := 'GAIN_GAINI_8x';
    Result.rbyte := 'GAINI';
  end;
  if Tp = TYPE_GAIN_GAINP then begin  // GAINP
    if S = '1x'
      then Result.rbit := 'GAIN_GAINP_1x';
    if S = '2x'
      then Result.rbit := 'GAIN_GAINP_2x';
    if S = '4x'
      then Result.rbit := 'GAIN_GAINP_4x';
    if S = '8x'
      then Result.rbit := 'GAIN_GAINP_8x';
    Result.rbyte := 'GAINP';
  end;
  if Tp = TYPE_FAN_SPIN_UP_TIME then begin  // SPIN_TIME
    if S = '250ms'
      then Result.rbit := 'FAN_SPIN_UP_TIME1';
    if S = '500ms'
      then Result.rbit := 'FAN_SPIN_UP_TIME2';
    if S = '1s'
      then Result.rbit := 'FAN_SPIN_UP_TIME3';
    if S = '2s'
      then Result.rbit := 'FAN_SPIN_UP_TIME4';
    Result.rbyte := 'FAN_SPIN_UP_TIME';
  end;
  if Tp = TYPE_FAN_SPIN_UP_LVL then begin  // SPIN_LVL
    if S = '30%'
      then Result.rbit := 'FAN_SPIN_UP_LVL1';
    if S = '35%'
      then Result.rbit := 'FAN_SPIN_UP_LVL2';
    if S = '40%'
      then Result.rbit := 'FAN_SPIN_UP_LVL3';
    if S = '45%'
      then Result.rbit := 'FAN_SPIN_UP_LVL4';
    if S = '50%'
      then Result.rbit := 'FAN_SPIN_UP_LVL5';
    if S = '55%'
      then Result.rbit := 'FAN_SPIN_UP_LVL6';
    if S = '60%'
      then Result.rbit := 'FAN_SPIN_UP_LVL7';
    if S = '65%'
      then Result.rbit := 'FAN_SPIN_UP_LVL8';
    Result.rbyte := 'FAN_SPIN_UP_LVL';
  end;
  if Tp = TYPE_FAN_SPIN_UP_NOKICK then begin  // SPIN_NOKICK
    if S = 'SPIN'
      then Result.rbit := 'FAN_SPIN_UP_SPIN';
    if S = 'NO_SPIN'
      then Result.rbit := 'FAN_SPIN_UP_NO_SPIN';
    Result.rbyte := 'FAN_SPIN_UP_NOKICK';
  end;
  if Tp = TYPE_FAN_SPIN_UP_DRIVE_FAIL then begin  // DRIVE_FAIL
    if S = 'DISABLE'
      then Result.rbit := 'FAN_SPIN_UP_DF1';
    if S = '16UP_PER'
      then Result.rbit := 'FAN_SPIN_UP_DF2';
    if S = '32UP_PER'
      then Result.rbit := 'FAN_SPIN_UP_DF3';
    if S = '64UP_PER'
      then Result.rbit := 'FAN_SPIN_UP_DF4';
    Result.rbyte := 'FAN_SPIN_UP_DRIVE_FAIL_CNT';
  end;
  if Tp = TYPE_FAN_STAT_INT  then begin  // STAT_INT
    if S = 'ALERT'
      then Result.rbyte := 'FAN_INT_EN';
    if S = 'NO_ALERT'
      then Result.rbyte := 'FAN_INT_EN_CLR';
  end;
  if Tp = TYPE_FAN_PWM_POLARITY  then begin  // PWM_POLARITY
    if S = 'INVERTED'
      then Result.rbyte := 'POLARITY';
    if S = 'NORMAL'
      then Result.rbyte := 'POLARITY_CLR';
  end;
  if Tp = TYPE_FAN_PWM_OUTPUT  then begin  // PWM_OUTPUT
    if S = 'PUSH-PULL'
      then Result.rbyte := 'PWM_OT';
    if S = 'OPEN-DRAIN'
      then Result.rbyte := 'PWM_OT_CLR';
  end;
  if Tp = TYPE_FAN_PWM_BASE  then begin  // PWM_BASE
    if S = '26.00kHz'
      then Result.rbit := 'FAN_PWM_BASE1';
    if S = '19.531kHz'
      then Result.rbit := 'FAN_PWM_BASE2';
    if S = '4.882Hz'
      then Result.rbit := 'FAN_PWM_BASE3';
    if S = '2.441Hz'
      then Result.rbit := 'FAN_PWM_BASE4';
    Result.rbyte := 'BASE';
  end;
  if Tp = TYPE_LOCKED  then begin  // SOFTWARE_LOCK
    if S = 'UNLOCKED'
      then Result.rbyte := 'LOCK_CLR';
    if S = 'LOCKED'
      then Result.rbyte := 'LOCK';
  end;
end;

end.

