unit help;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, ExtCtrls;

type

  { TForm_help }

  TForm_help = class(TForm)
    Image_mode1: TImage;
    Image_monitor: TImage;
    Image_smsc_logo: TImage;
    Image_microchip_logo: TImage;
    Image_mode: TImage;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
  private
  public
  end;

var
  Form_help: TForm_help;

implementation

{$R *.lfm}

{ TForm_help }

end.

