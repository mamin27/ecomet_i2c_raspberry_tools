unit help;

{$mode objfpc}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, ExtCtrls;

type

  { TForm_help }

  TForm_help = class(TForm)
    Image_ti_logo: TImage;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    procedure Image_ti_logoClick(Sender: TObject);
    procedure Label2Click(Sender: TObject);
  private

  public

  end;

var
  Form_help: TForm_help;

implementation

{$R *.lfm}

{ TForm_help }

procedure TForm_help.Image_ti_logoClick(Sender: TObject);
begin
  sleep(10000);
end;

procedure TForm_help.Label2Click(Sender: TObject);
begin

end;

end.

