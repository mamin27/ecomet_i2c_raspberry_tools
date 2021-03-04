unit emc2301_read;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons, Math,
  emc2301_pyth_util, emc2301_display;

procedure read_output_emc (emc: emc2301Ob);
procedure read_speed_emc (emc: emc2301Ob);
procedure read_emc ();
procedure read_speed ();
procedure self_test ();
function EnumToInt (Tp: Integer; S: String) : Integer;

Implementation

const

  TYPE_MASK = 0;
  TYPE_ENABLE = 1;
  TYPE_DISABLE = 2;
  TYPE_OPER = 3;
  TYPE_DR_CLK = 4;
  TYPE_USE_CLK = 5;
  TYPE_EN_ALGO = 6;
  TYPE_RANGE = 7;
  TYPE_EDGE = 8;
  TYPE_UPDATE = 9;
  TYPE_DER_OPT = 10;
  TYPE_ERR_RNG = 11;
  TYPE_GAIN = 12;
  TYPE_SPIN_FAIL = 13;
  TYPE_SPIN_NOKICK = 14;
  TYPE_SPIN_LVL = 15;
  TYPE_SPIN_TIME = 16;
  TYPE_STAT_WATCH = 17;
  TYPE_STAT_FAIL = 18;
  TYPE_STAT_FAILI = 19;
  TYPE_STAT_SPIN = 20;
  TYPE_STAT_STALL = 21;
  TYPE_STAT_INT = 22;
  TYPE_PWM_POLARITY = 23;
  TYPE_PWM_OUTPUT = 24;
  TYPE_PWM_BASE = 25;

  TYPE_LOCK = 26;

  TYPE_MON_SAMPLE = 100;

function EnumToInt (Tp: Integer; S: String) : Integer;
begin
  if Tp = TYPE_MASK then begin  // MASK
    if S = 'MASKED'
      then Result := 0;
    if S = 'UNMASKED'
      then Result := 1;
  end;
  if Tp = TYPE_ENABLE then begin  // ENABLE
    if S = 'DISABLED'
      then Result := 0;
    if S = 'ENABLED'
      then Result := 1;
  end;
  if Tp = TYPE_DISABLE then begin  // DISABLED
    if S = 'ENABLED'
      then Result := 0;
    if S = 'DISABLED'
      then Result := 1;
  end;
  if Tp = TYPE_OPER then begin  // OPER
    if S = 'OPERATE'
      then Result := 0;
    if S = 'DISABLED'
      then Result := 1;
  end;
  if Tp = TYPE_DR_CLK then begin  // DR_CLK
    if S = 'CLK_OUTPUT'
      then Result := 0;
    if S = 'CLK_INPUT'
      then Result := 1;
  end;
  if Tp = TYPE_USE_CLK then begin  // USE_CLK
    if S = 'EXTERNAL'
      then Result := 0;
    if S = 'INTERNAL'
      then Result := 1;
  end;
  if Tp = TYPE_EN_ALGO then begin  // EN_ALGO
    if S = 'DISABLED'
      then Result := 0;
    if S = 'ENABLED'
      then Result := 1;
  end;
  if Tp = TYPE_RANGE then begin  // RANGE
    if S = '500>1'
      then Result := 0;
    if S = '1000>2'
      then Result := 1;
    if S = '2000>4'
      then Result := 2;
    if S = '4000>8'
      then Result := 3;
  end;
  if Tp = TYPE_EDGE then begin  // EDGE
    if S = '3>1POLE>0.5'
      then Result := 0;
    if S = '5>2POLE>1'
      then Result := 1;
    if S = '7>3POLE>1.5'
      then Result := 2;
    if S = '9>4POLE>2'
      then Result := 3;
  end;
  if Tp = TYPE_UPDATE then begin  // UPDATE
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
  if Tp = TYPE_DER_OPT then begin  // DER_OPT
    if S = 'NO_DERIVATE'
      then Result := 0;
    if S = 'BASIC_DERIVATE'
      then Result := 1;
    if S = 'STEP_DERIVATE'
      then Result := 2;
    if S = 'BOTH_DERIVATE'
      then Result := 3;
  end;
  if Tp = TYPE_ERR_RNG then begin  // ERR_RNG
    if S = '0RPM'
      then Result := 0;
    if S = '50RPM'
      then Result := 1;
    if S = '100RPM'
      then Result := 2;
    if S = '200RPM'
      then Result := 3;
  end;
  if Tp = TYPE_GAIN then begin  // GAIN
    if S = '1x'
      then Result := 0;
    if S = '2x'
      then Result := 1;
    if S = '4x'
      then Result := 2;
    if S = '8x'
      then Result := 3;
  end;
  if Tp = TYPE_SPIN_FAIL then begin  // SPIN_FAIL
    if S = 'DISABLE'
      then Result := 0;
    if S = '16UP_PER'
      then Result := 1;
    if S = '32UP_PER'
      then Result := 2;
    if S = '64UP_PER'
      then Result := 3;
  end;
  if Tp = TYPE_SPIN_NOKICK then begin  // SPIN_NOKICK
    if S = 'SPIN'
      then Result := 0;
    if S = 'NO_SPIN'
      then Result := 1;
  end;
  if Tp = TYPE_SPIN_LVL then begin  // SPIN_LVL
    if S = '30%'
      then Result := 0;
    if S = '35%'
      then Result := 1;
    if S = '40%'
      then Result := 2;
    if S = '45%'
      then Result := 3;
    if S = '50%'
      then Result := 4;
    if S = '55%'
      then Result := 5;
    if S = '60%'
      then Result := 6;
    if S = '65%'
      then Result := 7;
  end;
  if Tp = TYPE_SPIN_TIME then begin  // SPIN_TIME
    if S = '250ms'
      then Result := 0;
    if S = '500ms'
      then Result := 1;
    if S = '1s'
      then Result := 2;
    if S = '2s'
      then Result := 3;
  end;
  if Tp = TYPE_STAT_WATCH then begin  // STAT_WATCH
    if S = 'EXPIRED'
      then Result := 0;
    if S = 'NOT_SET'
      then Result := 1;
  end;
  if Tp = TYPE_STAT_FAIL then begin  // STAT_FAIL
    if S = 'CANOT_MEET'
      then Result := 0;
    if S = 'MEET'
      then Result := 1;
  end;
  if Tp = TYPE_STAT_FAILI then begin  // STAT_FAILI
    if S = 'CANOT_REACH'
      then Result := 0;
    if S = 'REACH'
      then Result := 1;
  end;
  if Tp = TYPE_STAT_SPIN then begin  // STAT_SPIN
    if S = 'CANOT_SPIN'
      then Result := 0;
    if S = 'SPIN'
      then Result := 1;
  end;
  if Tp = TYPE_STAT_STALL then begin  // STAT_STALL
    if S = 'STALL'
      then Result := 0;
    if S = 'NOT_STALL'
      then Result := 1;
  end;
  if Tp = TYPE_STAT_INT then begin  // STAT_INT
    if S = 'ALERT'
      then Result := 0;
    if S = 'NO_ALERT'
      then Result := 1;
  end;
  if Tp = TYPE_PWM_POLARITY then begin  // PWM_POLARITY
    if S = 'INVERTED'
      then Result := 0;
    if S = 'NORMAL'
      then Result := 1;
  end;
  if Tp = TYPE_PWM_OUTPUT then begin  // PWM_OUTPUT
    if S = 'PUSH-PULL'
      then Result := 0;
    if S = 'OPEN-DRAIN'
      then Result := 1;
  end;
  if Tp = TYPE_PWM_BASE then begin  // PWM_BASE
    if S = '26.00kHz'
      then Result := 0;
    if S = '19.531kHz'
      then Result := 1;
    if S = '4.882Hz'
      then Result := 2;
    if S = '2.441Hz'
      then Result := 3;
  end;
  if Tp = TYPE_MON_SAMPLE then begin  // MON_SAMPLE
    if S = 'off'
      then Result := 0;
    if S = '1s'
      then Result := 1;
    if S = '3s'
      then Result := 3;
    if S = '10s'
      then Result := 10;
    if S = '20s'
      then Result := 20;
  end;
  if Tp = TYPE_LOCK then begin  // LOCKED
    if S = 'UNLOCKED'
      then Result := 0;
    if S = 'LOCKED'
      then Result := 1;
  end;
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

procedure read_speed ();
var
  Py_S: TStringList;
begin
Py_S := TStringList.Create;
Py_S.Delimiter := '|';
Py_S.StrictDelimiter := True;
Py_S.DelimitedText := 'from  i2c_pkg.emc2301_pkg import emc2301|' +
                      'from time import sleep|' +
                      'import statistics|' +
                      'sens = emc2301.EMC2301()|' +
                      'measure = []|' +
                      'for i in range (10) :|' +
                      '  measure.append(sens.speed()[0])|' +
                      '  sleep(0.01)|' +
                      'print (":READ_speed:SPEED::RPM::{}".format(int(statistics.mean(measure))))|';

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
  Form_emc2301.CB_CONF_EN_ALGO.ItemIndex := EnumToInt(TYPE_ENABLE,emc.attr1.attr_val_obj.attr6.attr_val);     //EN_ALGE 0-DISABLED, 1-ENABLED
  Form_emc2301.CB_CONF_RANGE.ItemIndex := EnumToInt(TYPE_RANGE,emc.attr1.attr_val_obj.attr7.attr_val);     //RANGE
  Form_emc2301.CB_CONF_EDGES.ItemIndex := EnumToInt(TYPE_EDGE,emc.attr1.attr_val_obj.attr8.attr_val);     //EDGE
  Form_emc2301.CB_CONF_UPDATE.ItemIndex := EnumToInt(TYPE_UPDATE,emc.attr1.attr_val_obj.attr9.attr_val);     //UPDATE
  Form_emc2301.CB_CONF_EN_RRC.ItemIndex := EnumToInt(TYPE_DISABLE,emc.attr1.attr_val_obj.attr10.attr_val);     //EN_RRC 0-ENABLED, 1-DISABLED
  Form_emc2301.CB_CONF_GLITCH_EN.ItemIndex := EnumToInt(TYPE_DISABLE,emc.attr1.attr_val_obj.attr11.attr_val);     //GLITCH_EN 0-ENABLED, 1-DISABLED
  Form_emc2301.CB_CONF_DER_OPT.ItemIndex := EnumToInt(TYPE_DER_OPT,emc.attr1.attr_val_obj.attr12.attr_val);     //DER_OPT
  Form_emc2301.CB_CONF_ERR_RNG.ItemIndex := EnumToInt(TYPE_ERR_RNG,emc.attr1.attr_val_obj.attr13.attr_val);     //ERR_RNG
  Form_emc2301.CB_GN_GAIND.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr14.attr_val);     //GAIND
  Form_emc2301.CB_GN_GAINI.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr15.attr_val);     //GAINI
  Form_emc2301.CB_GN_GAINP.ItemIndex := EnumToInt(TYPE_GAIN,emc.attr1.attr_val_obj.attr16.attr_val);     //GAINP

  Form_emc2301.ET_STAT_WATCH.Text := emc.attr2.attr_val_obj.attr1.attr_val;     //WATCH
  Form_emc2301.ET_STAT_DRIVE_FAIL.Text := emc.attr2.attr_val_obj.attr2.attr_val;     //DRIVE_FAIL
  Form_emc2301.ET_STAT_FAN_SPIN.Text := emc.attr2.attr_val_obj.attr3.attr_val;     //FAN_SPIN
  Form_emc2301.ET_STAT_FAN_STALL.Text := emc.attr2.attr_val_obj.attr4.attr_val;     //FAN_STALL
  Form_emc2301.CB_STAT_FAN_INT.ItemIndex := EnumToInt(TYPE_STAT_INT,emc.attr2.attr_val_obj.attr5.attr_val);     //FAN_INT
  Form_emc2301.ET_STAT_FAN_SETTING.Text := FloatToStr(RoundTo(StrToFloat(emc.attr2.attr_val_obj.attr6.attr_val),-1));     //FAN_SETTING

  Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.ItemIndex := EnumToInt(TYPE_SPIN_FAIL,emc.attr3.attr_val_obj.attr1.attr_val);     //DRIVE_FAIL_CNT
  Form_emc2301.CB_SPIN_NOKICK.ItemIndex := EnumToInt(TYPE_SPIN_NOKICK,emc.attr3.attr_val_obj.attr2.attr_val);     //NOKICK
  Form_emc2301.CB_SPIN_LVL.ItemIndex := EnumToInt(TYPE_SPIN_LVL,emc.attr3.attr_val_obj.attr3.attr_val);     //SPIN_LVL
  Form_emc2301.CB_SPIN_TIME.ItemIndex := EnumToInt(TYPE_SPIN_TIME,emc.attr3.attr_val_obj.attr4.attr_val);     //SPINUP_TIME
  Form_emc2301.ET_SPIN_FAN_MAX_STEP.Text := emc.attr3.attr_val_obj.attr5.attr_val;     //SPIN_FAN_MAX_STEP
  Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.Text := emc.attr3.attr_val_obj.attr6.attr_val;     //SPIN_FAN_MIN_DRIVE

  Form_emc2301.CB_PWM_POLARITY.ItemIndex := EnumToInt(TYPE_PWM_POLARITY,emc.attr4.attr_val_obj.attr1.attr_val);     //PWM_POLARITY
  Form_emc2301.CB_PWM_OUTPUT.ItemIndex := EnumToInt(TYPE_PWM_OUTPUT,emc.attr4.attr_val_obj.attr2.attr_val);     //PWM_OUTPUT
  Form_emc2301.CB_PWM_BASE.ItemIndex := EnumToInt(TYPE_PWM_BASE,emc.attr4.attr_val_obj.attr3.attr_val);     //PWM_BASE
  Form_emc2301.ET_PWM_DIVIDE.Text := emc.attr4.attr_val_obj.attr4.attr_val;     //PWM_DIVIDE

  Form_emc2301.ET_TACH_COUNT.Text := emc.attr5.attr_val_obj.attr1.attr_val;     //TACH_COUNT
  Form_emc2301.ET_TACH_FAN_FAIL_BAND.Text := emc.attr5.attr_val_obj.attr2.attr_val;     //TACH_FAN_FAIL_BAND
  Form_emc2301.ET_TACH_TARGET.Text := emc.attr5.attr_val_obj.attr3.attr_val;     //TACH_TARGET

  Form_emc2301.ET_ID_PRODUCT.Text := emc.attr6.attr_val_obj.attr1.attr_val;     //PRODUCT_ID
  Form_emc2301.ET_ID_MANUF.Text := emc.attr6.attr_val_obj.attr2.attr_val;     //MANUF_ID
  Form_emc2301.ET_ID_REVISION.Text := emc.attr6.attr_val_obj.attr3.attr_val;     //REVISION_ID

  Form_emc2301.CB_LOCK.ItemIndex := EnumToInt(TYPE_LOCK,emc.attr7.attr_val_obj.attr1.attr_val);     //SOFTWARE_LOCK


(*
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
  Form_emc2301.CB_GN_GAIND.Style := csOwnerDrawVariable;
  Form_emc2301.CB_GN_GAINI.Style := csOwnerDrawVariable;
  Form_emc2301.CB_GN_GAINP.Style := csOwnerDrawVariable;
*)

  Form_emc2301.ET_STAT_WATCH.Color := clMenubar;     //WATCH
  Form_emc2301.ET_STAT_DRIVE_FAIL.Color := clMenubar;     //DRIVE_FAIL
  Form_emc2301.ET_STAT_FAN_SPIN.Color := clMenubar;     //FAN_SPIN
  Form_emc2301.ET_STAT_FAN_STALL.Color := clMenubar;  //FAN_STALL
  Form_emc2301.ET_ID_PRODUCT.Color := clMenubar;     //PRODUCT_ID
  Form_emc2301.ET_ID_MANUF.Color := clMenubar;     //MANUF_ID
  Form_emc2301.ET_ID_REVISION.Color := clMenubar;  //REVISION_ID

  if (Form_emc2301.CB_LOCK.ItemIndex = 1 ) then
  begin
//    Form_emc2301.CB_CONF_MASK.Color := clMenubar;     //CONF_MASK
//    Form_emc2301.CB_CONF_MASK.ReadOnly := True;
    Form_emc2301.CB_CONF_DIS_TO.Color := clMenubar;     //CONF_DIS_TO
    Form_emc2301.CB_CONF_DIS_TO.Style := csOwnerDrawFixed;
    Form_emc2301.CB_CONF_WD_EN.Color := clMenubar;     //CONF_WD_EN
    Form_emc2301.CB_CONF_WD_EN.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_DR_EXT_CLK.Color := clMenubar;     //CONF_DR_EXT_CLK
    Form_emc2301.CB_CONF_DR_EXT_CLK.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_USE_EXT_CLK.Color := clMenubar;  //CONF_USE_EXT_CLK
    Form_emc2301.CB_CONF_USE_EXT_CLK.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_EN_RRC.Color := clMenubar;     //CONF2EN_RRC
    Form_emc2301.CB_CONF_EN_RRC.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_GLITCH_EN.Color := clMenubar;     //CONF2_GLITCH_EN
    Form_emc2301.CB_CONF_GLITCH_EN.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_DER_OPT.Color := clMenubar;  //CONF2_DER_OPT
    Form_emc2301.CB_CONF_DER_OPT.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_CONF_ERR_RNG.Color := clMenubar;     //CONF2_ERR_RNG
    Form_emc2301.CB_CONF_ERR_RNG.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_GN_GAIND.Color := clMenubar;     //GAIND
    Form_emc2301.CB_GN_GAIND.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_GN_GAINI.Color := clMenubar;     //GAINI
    Form_emc2301.CB_GN_GAINI.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_GN_GAINP.Color := clMenubar;     //GAINP
    Form_emc2301.CB_GN_GAINP.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_SPIN_TIME.Color := clMenubar;  //SPINUP_TIME
    Form_emc2301.CB_SPIN_TIME.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_SPIN_LVL.Color := clMenubar;     //SPINUP_LVL
    Form_emc2301.CB_SPIN_LVL.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_SPIN_NOKICK.Color := clMenubar;     //SPINUP_NOKICK
    Form_emc2301.CB_SPIN_NOKICK.Style:= csOwnerDrawFixed;
    Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.Color := clMenubar;  //SPINUP_DRIVE_FAIL_CNT
    Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.Style:= csOwnerDrawFixed;
    Form_emc2301.ET_SPIN_FAN_MAX_STEP.Color := clMenubar;     //SPINUP_FAN_MAX_STEP
    Form_emc2301.ET_SPIN_FAN_MAX_STEP.ReadOnly:= True;
    Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.Color := clMenubar;     //SPINUP_FAN_MIN_DRIVE
    Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.ReadOnly:= True;
    Form_emc2301.ET_TACH_COUNT.Color := clMenubar;     //TACH_COUNT
    Form_emc2301.ET_TACH_COUNT.ReadOnly:= True;
    Form_emc2301.ET_TACH_FAN_FAIL_BAND.Color := clMenubar;     //TACH_FAN_FAIL_BAND
    Form_emc2301.ET_TACH_FAN_FAIL_BAND.ReadOnly:= True;
    Form_emc2301.CB_LOCK.Color := clMenubar;  // SOFTWARE_LOCK
    Form_emc2301.CB_LOCK.Style:= csOwnerDrawFixed;
  end
  else begin
    Form_emc2301.CB_CONF_DIS_TO.Color := clDefault;     //CONF_DIS_TO
    Form_emc2301.CB_CONF_DIS_TO.Style := csDropDown;
    Form_emc2301.CB_CONF_WD_EN.Color := clDefault;     //CONF_WD_EN
    Form_emc2301.CB_CONF_WD_EN.Style:= csDropDown;
    Form_emc2301.CB_CONF_DR_EXT_CLK.Color := clDefault;     //CONF_DR_EXT_CLK
    Form_emc2301.CB_CONF_DR_EXT_CLK.Style:= csDropDown;
    Form_emc2301.CB_CONF_USE_EXT_CLK.Color := clDefault;  //CONF_USE_EXT_CLK
    Form_emc2301.CB_CONF_USE_EXT_CLK.Style:= csDropDown;
    Form_emc2301.CB_CONF_EN_RRC.Color := clDefault;     //CONF2EN_RRC
    Form_emc2301.CB_CONF_EN_RRC.Style:= csDropDown;
    Form_emc2301.CB_CONF_GLITCH_EN.Color := clDefault;     //CONF2_GLITCH_EN
    Form_emc2301.CB_CONF_GLITCH_EN.Style:= csDropDown;
    Form_emc2301.CB_CONF_DER_OPT.Color := clDefault;  //CONF2_DER_OPT
    Form_emc2301.CB_CONF_DER_OPT.Style:= csDropDown;
    Form_emc2301.CB_CONF_ERR_RNG.Color := clDefault;     //CONF2_ERR_RNG
    Form_emc2301.CB_CONF_ERR_RNG.Style:= csDropDown;
    Form_emc2301.CB_GN_GAIND.Color := clDefault;     //GAIND
    Form_emc2301.CB_GN_GAIND.Style:= csDropDown;
    Form_emc2301.CB_GN_GAINI.Color := clDefault;     //GAINI
    Form_emc2301.CB_GN_GAINI.Style:= csDropDown;
    Form_emc2301.CB_GN_GAINP.Color := clDefault;     //GAINP
    Form_emc2301.CB_GN_GAINP.Style:= csDropDown;
    Form_emc2301.CB_SPIN_TIME.Color := clDefault;  //SPINUP_TIME
    Form_emc2301.CB_SPIN_TIME.Style:= csDropDown;
    Form_emc2301.CB_SPIN_LVL.Color := clDefault;     //SPINUP_LVL
    Form_emc2301.CB_SPIN_LVL.Style:= csDropDown;
    Form_emc2301.CB_SPIN_NOKICK.Color := clDefault;     //SPINUP_NOKICK
    Form_emc2301.CB_SPIN_NOKICK.Style:= csDropDown;
    Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.Color := clDefault;  //SPINUP_DRIVE_FAIL_CNT
    Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.Style:= csDropDown;
    Form_emc2301.ET_SPIN_FAN_MAX_STEP.Color := clDefault;     //SPINUP_FAN_MAX_STEP
    Form_emc2301.ET_SPIN_FAN_MAX_STEP.ReadOnly:= False;
    Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.Color := clDefault;     //SPINUP_FAN_MIN_DRIVE
    Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.ReadOnly:= False;
    Form_emc2301.ET_TACH_COUNT.Color := clDefault;     //TACH_COUNT
    Form_emc2301.ET_TACH_COUNT.ReadOnly:= False;
    Form_emc2301.ET_TACH_FAN_FAIL_BAND.Color := clDefault;     //TACH_FAN_FAIL_BAND
    Form_emc2301.ET_TACH_FAN_FAIL_BAND.ReadOnly:= False;
    Form_emc2301.CB_LOCK.Color := clDefault;  // SOFTWARE_LOCK
    Form_emc2301.CB_LOCK.Style:= csDropDown;
  end;

//  Form_emc2301.Edit_serial.Text:= emc.attr2.attr_val_obj.attr1.attr_val;  //SERIAL
//  Form_emc2301.Edit_serial.Alignment:=taRightJustify;
//  Form_emc2301.Edit_manuf.Text:= emc.attr2.attr_val_obj.attr2.attr_val;  //MANUFACTURER
//  Form_emc2301.Edit_manuf.Alignment:=taRightJustify;
//  Form_emc2301.Edit_devid.Text:= emc.attr2.attr_val_obj.attr3.attr_val;  //DEVICE ID
//  Form_emc2301.Edit_devid.Alignment:=taRightJustify;

end;
procedure read_speed_emc (emc: emc2301Ob);
begin
  Form_emc2301.ET_TACH_READ.Text := emc.attr8.attr_val_obj.attr1.attr_val;     //RPM
//  writeln(emc.attr7.attr_val_obj.attr1.attr_val);
  Form_emc2301.BitBtn_MON.ImageIndex:= 0;
end;

end.

