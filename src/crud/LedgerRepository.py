from sqlalchemy.orm import Session

from src.dto.LedgerDto import RequestLedgerCreate, RequestLedgerUpdate
from src.entity.Model import UserLogin, Ledger
from src.interface.Interface import AppRepository


class LedgerRepository(AppRepository):

    def create_ledger(self, ledger: RequestLedgerCreate, current_user: UserLogin):
        ledger = Ledger(
            price=ledger.price,
            memo=ledger.memo,
            user=current_user
        )
        self.db.add(ledger)
        self.db.commit()
        return ledger

    def get_all_ledgers(self, current_user: UserLogin):
        return self.db.query(Ledger).filter(Ledger.user_id == current_user.id).all()

    def get_ledger(self, ledger_id: int, current_user: UserLogin):
        return self.db.query(Ledger).filter(
            Ledger.id == ledger_id
        ).filter(Ledger.user_id == current_user.id).one()

    def modify_ledger(self,
                      ledger_id: int,
                      updated_ledger: RequestLedgerUpdate, current_user: UserLogin):

        selected_ledger = self.get_ledger(ledger_id=ledger_id, current_user=current_user)
        if updated_ledger.memo:
            selected_ledger.memo = updated_ledger.memo
        if updated_ledger.price:
            selected_ledger.price = updated_ledger.price

        self.db.add(selected_ledger)
        self.db.commit()

    def delete_ledger(self, ledger_id: int, current_user: UserLogin):
        self.db.query(Ledger).filter(Ledger.id == ledger_id) \
            .filter(
            Ledger.user_id == current_user.id
        ).delete()
        self.db.commit()
