import datetime
from decimal import Decimal
from django.db import models
from categories . models import Category, StandardMetadata, ActiveManager
from transactions . models import Transaction
from django.utils.translation import ugettext_lazy as _


class BudgetManager(ActiveManager):
    def get_queryset(self, date):
        return super(BudgetManager, self).get_queryset().filter(start_date__lte=date).latest('start_date')

class Budget(StandardMetadata):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    start_date = models.DateTimeField(_('Start Date'), default=datetime.datetime.now, db_index=True)
    objects = models.Manager()
    active = BudgetManager()

    def __str__(self):
        return self.name

    def monthly_estimated_total(self):
        total = Decimal('0.0')
        for estimate in self.estimates.exclude(is_deleted=True):
            total += estimate.amount
        return total

    def yearly_estimated_total(self):
        return self.monthly_estimated_total() * 12

    def estimates_and_transactions(self, start_date, end_date):
        estimates_and_transactions = []
        actual_total = Decimal('0.0')

        for estimate in self.estimates.exclude(is_deleted=True):
            actual_amount = estimate.actual_amount(start_date, end_date)
            actual_total += actual_amount
            estimates_and_transactions.append({
                'estimate': estimate,
                'transactions': estimate.actual_transactions(start_date, end_date),
                'actual_amount': actual_amount,
            })
        return (estimates_and_transactions, actual_total)

    def actual_total(self, start_date, end):
        actual_total = Decimal('0.0')
        for estimate in self.estimates.exclude(is_deleted=True):
            actual_amount = estimate.actual_amount(start_date, end_date)
            actual_total += actual_amount
        return actual_total

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')


class BudgetEstimate(StandardMetadata):
    # individual items that makes up a budget
    budget = models.ForeignKey(Budget, related_name='estimates', verbose_name=_('Budget'), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='estimates', verbose_name=_('Category'), on_delete=models.CASCADE)
    amount = models.DecimalField(_('Amount'), max_digits=11, decimal_places=2)
    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return u"%s - %s" % (self.category.name, self.amount)

    def yearly_estimated_amount(self):
        return self.amount * 12

    def actual_transactions(self, start_date, end_date):
        # estimates should only report on espenses
        return Transactions.expenses.filter(category=self.category, date__range=(start_date, end_date)).order_by('date')

    def actual_amount(self, start_date, end_date):
        total = Decimal('0.0')
        for transaction in self.actual_transactions(start_date, end_date):
            total += transaction.amount
        return total

    class Meta:
        verbose_name = _('Budget estimate')
        verbose_name_plural = _('Budget estimates')
