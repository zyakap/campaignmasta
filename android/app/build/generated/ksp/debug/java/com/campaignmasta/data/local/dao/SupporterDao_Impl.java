package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.SupporterEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class SupporterDao_Impl implements SupporterDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<SupporterEntity> __insertionAdapterOfSupporterEntity;

  private final EntityDeletionOrUpdateAdapter<SupporterEntity> __updateAdapterOfSupporterEntity;

  private final SharedSQLiteStatement __preparedStmtOfMarkSynced;

  private final SharedSQLiteStatement __preparedStmtOfMarkFailed;

  private final SharedSQLiteStatement __preparedStmtOfDelete;

  public SupporterDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfSupporterEntity = new EntityInsertionAdapter<SupporterEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `supporters` (`localId`,`serverId`,`fullName`,`gender`,`ageRange`,`phone`,`ward`,`wardId`,`village`,`villageId`,`clan`,`enrollmentStatus`,`supportStatus`,`notes`,`followUpRequired`,`followUpDate`,`consentToMessages`,`updatedAt`,`syncStatus`,`createdLocallyAt`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final SupporterEntity entity) {
        statement.bindString(1, entity.getLocalId());
        if (entity.getServerId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getServerId());
        }
        statement.bindString(3, entity.getFullName());
        statement.bindString(4, entity.getGender());
        statement.bindString(5, entity.getAgeRange());
        statement.bindString(6, entity.getPhone());
        statement.bindString(7, entity.getWard());
        if (entity.getWardId() == null) {
          statement.bindNull(8);
        } else {
          statement.bindLong(8, entity.getWardId());
        }
        statement.bindString(9, entity.getVillage());
        if (entity.getVillageId() == null) {
          statement.bindNull(10);
        } else {
          statement.bindLong(10, entity.getVillageId());
        }
        statement.bindString(11, entity.getClan());
        statement.bindString(12, entity.getEnrollmentStatus());
        statement.bindString(13, entity.getSupportStatus());
        statement.bindString(14, entity.getNotes());
        final int _tmp = entity.getFollowUpRequired() ? 1 : 0;
        statement.bindLong(15, _tmp);
        if (entity.getFollowUpDate() == null) {
          statement.bindNull(16);
        } else {
          statement.bindString(16, entity.getFollowUpDate());
        }
        final int _tmp_1 = entity.getConsentToMessages() ? 1 : 0;
        statement.bindLong(17, _tmp_1);
        statement.bindString(18, entity.getUpdatedAt());
        statement.bindString(19, entity.getSyncStatus());
        statement.bindLong(20, entity.getCreatedLocallyAt());
      }
    };
    this.__updateAdapterOfSupporterEntity = new EntityDeletionOrUpdateAdapter<SupporterEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `supporters` SET `localId` = ?,`serverId` = ?,`fullName` = ?,`gender` = ?,`ageRange` = ?,`phone` = ?,`ward` = ?,`wardId` = ?,`village` = ?,`villageId` = ?,`clan` = ?,`enrollmentStatus` = ?,`supportStatus` = ?,`notes` = ?,`followUpRequired` = ?,`followUpDate` = ?,`consentToMessages` = ?,`updatedAt` = ?,`syncStatus` = ?,`createdLocallyAt` = ? WHERE `localId` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final SupporterEntity entity) {
        statement.bindString(1, entity.getLocalId());
        if (entity.getServerId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getServerId());
        }
        statement.bindString(3, entity.getFullName());
        statement.bindString(4, entity.getGender());
        statement.bindString(5, entity.getAgeRange());
        statement.bindString(6, entity.getPhone());
        statement.bindString(7, entity.getWard());
        if (entity.getWardId() == null) {
          statement.bindNull(8);
        } else {
          statement.bindLong(8, entity.getWardId());
        }
        statement.bindString(9, entity.getVillage());
        if (entity.getVillageId() == null) {
          statement.bindNull(10);
        } else {
          statement.bindLong(10, entity.getVillageId());
        }
        statement.bindString(11, entity.getClan());
        statement.bindString(12, entity.getEnrollmentStatus());
        statement.bindString(13, entity.getSupportStatus());
        statement.bindString(14, entity.getNotes());
        final int _tmp = entity.getFollowUpRequired() ? 1 : 0;
        statement.bindLong(15, _tmp);
        if (entity.getFollowUpDate() == null) {
          statement.bindNull(16);
        } else {
          statement.bindString(16, entity.getFollowUpDate());
        }
        final int _tmp_1 = entity.getConsentToMessages() ? 1 : 0;
        statement.bindLong(17, _tmp_1);
        statement.bindString(18, entity.getUpdatedAt());
        statement.bindString(19, entity.getSyncStatus());
        statement.bindLong(20, entity.getCreatedLocallyAt());
        statement.bindString(21, entity.getLocalId());
      }
    };
    this.__preparedStmtOfMarkSynced = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE supporters SET serverId = ?, syncStatus = 'SYNCED' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfMarkFailed = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE supporters SET syncStatus = 'FAILED' WHERE localId = ?";
        return _query;
      }
    };
    this.__preparedStmtOfDelete = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "DELETE FROM supporters WHERE localId = ?";
        return _query;
      }
    };
  }

  @Override
  public Object insert(final SupporterEntity entity, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfSupporterEntity.insert(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object insertAll(final List<SupporterEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfSupporterEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object update(final SupporterEntity entity, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __updateAdapterOfSupporterEntity.handle(entity);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object markSynced(final String localId, final int serverId,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkSynced.acquire();
        int _argIndex = 1;
        _stmt.bindLong(_argIndex, serverId);
        _argIndex = 2;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkSynced.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object markFailed(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfMarkFailed.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfMarkFailed.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Object delete(final String localId, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfDelete.acquire();
        int _argIndex = 1;
        _stmt.bindString(_argIndex, localId);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfDelete.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<SupporterEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM supporters ORDER BY fullName ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"supporters"}, new Callable<List<SupporterEntity>>() {
      @Override
      @NonNull
      public List<SupporterEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfGender = CursorUtil.getColumnIndexOrThrow(_cursor, "gender");
          final int _cursorIndexOfAgeRange = CursorUtil.getColumnIndexOrThrow(_cursor, "ageRange");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfWard = CursorUtil.getColumnIndexOrThrow(_cursor, "ward");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfVillage = CursorUtil.getColumnIndexOrThrow(_cursor, "village");
          final int _cursorIndexOfVillageId = CursorUtil.getColumnIndexOrThrow(_cursor, "villageId");
          final int _cursorIndexOfClan = CursorUtil.getColumnIndexOrThrow(_cursor, "clan");
          final int _cursorIndexOfEnrollmentStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "enrollmentStatus");
          final int _cursorIndexOfSupportStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStatus");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfConsentToMessages = CursorUtil.getColumnIndexOrThrow(_cursor, "consentToMessages");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final List<SupporterEntity> _result = new ArrayList<SupporterEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final SupporterEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpGender;
            _tmpGender = _cursor.getString(_cursorIndexOfGender);
            final String _tmpAgeRange;
            _tmpAgeRange = _cursor.getString(_cursorIndexOfAgeRange);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpWard;
            _tmpWard = _cursor.getString(_cursorIndexOfWard);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpVillage;
            _tmpVillage = _cursor.getString(_cursorIndexOfVillage);
            final Integer _tmpVillageId;
            if (_cursor.isNull(_cursorIndexOfVillageId)) {
              _tmpVillageId = null;
            } else {
              _tmpVillageId = _cursor.getInt(_cursorIndexOfVillageId);
            }
            final String _tmpClan;
            _tmpClan = _cursor.getString(_cursorIndexOfClan);
            final String _tmpEnrollmentStatus;
            _tmpEnrollmentStatus = _cursor.getString(_cursorIndexOfEnrollmentStatus);
            final String _tmpSupportStatus;
            _tmpSupportStatus = _cursor.getString(_cursorIndexOfSupportStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final boolean _tmpConsentToMessages;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfConsentToMessages);
            _tmpConsentToMessages = _tmp_1 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _item = new SupporterEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpGender,_tmpAgeRange,_tmpPhone,_tmpWard,_tmpWardId,_tmpVillage,_tmpVillageId,_tmpClan,_tmpEnrollmentStatus,_tmpSupportStatus,_tmpNotes,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpConsentToMessages,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getPending(final Continuation<? super List<SupporterEntity>> $completion) {
    final String _sql = "SELECT * FROM supporters WHERE syncStatus = 'PENDING' ORDER BY createdLocallyAt ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<List<SupporterEntity>>() {
      @Override
      @NonNull
      public List<SupporterEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfGender = CursorUtil.getColumnIndexOrThrow(_cursor, "gender");
          final int _cursorIndexOfAgeRange = CursorUtil.getColumnIndexOrThrow(_cursor, "ageRange");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfWard = CursorUtil.getColumnIndexOrThrow(_cursor, "ward");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfVillage = CursorUtil.getColumnIndexOrThrow(_cursor, "village");
          final int _cursorIndexOfVillageId = CursorUtil.getColumnIndexOrThrow(_cursor, "villageId");
          final int _cursorIndexOfClan = CursorUtil.getColumnIndexOrThrow(_cursor, "clan");
          final int _cursorIndexOfEnrollmentStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "enrollmentStatus");
          final int _cursorIndexOfSupportStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStatus");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfConsentToMessages = CursorUtil.getColumnIndexOrThrow(_cursor, "consentToMessages");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final List<SupporterEntity> _result = new ArrayList<SupporterEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final SupporterEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpGender;
            _tmpGender = _cursor.getString(_cursorIndexOfGender);
            final String _tmpAgeRange;
            _tmpAgeRange = _cursor.getString(_cursorIndexOfAgeRange);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpWard;
            _tmpWard = _cursor.getString(_cursorIndexOfWard);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpVillage;
            _tmpVillage = _cursor.getString(_cursorIndexOfVillage);
            final Integer _tmpVillageId;
            if (_cursor.isNull(_cursorIndexOfVillageId)) {
              _tmpVillageId = null;
            } else {
              _tmpVillageId = _cursor.getInt(_cursorIndexOfVillageId);
            }
            final String _tmpClan;
            _tmpClan = _cursor.getString(_cursorIndexOfClan);
            final String _tmpEnrollmentStatus;
            _tmpEnrollmentStatus = _cursor.getString(_cursorIndexOfEnrollmentStatus);
            final String _tmpSupportStatus;
            _tmpSupportStatus = _cursor.getString(_cursorIndexOfSupportStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final boolean _tmpConsentToMessages;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfConsentToMessages);
            _tmpConsentToMessages = _tmp_1 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _item = new SupporterEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpGender,_tmpAgeRange,_tmpPhone,_tmpWard,_tmpWardId,_tmpVillage,_tmpVillageId,_tmpClan,_tmpEnrollmentStatus,_tmpSupportStatus,_tmpNotes,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpConsentToMessages,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object getByLocalId(final String localId,
      final Continuation<? super SupporterEntity> $completion) {
    final String _sql = "SELECT * FROM supporters WHERE localId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, localId);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<SupporterEntity>() {
      @Override
      @Nullable
      public SupporterEntity call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfGender = CursorUtil.getColumnIndexOrThrow(_cursor, "gender");
          final int _cursorIndexOfAgeRange = CursorUtil.getColumnIndexOrThrow(_cursor, "ageRange");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfWard = CursorUtil.getColumnIndexOrThrow(_cursor, "ward");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfVillage = CursorUtil.getColumnIndexOrThrow(_cursor, "village");
          final int _cursorIndexOfVillageId = CursorUtil.getColumnIndexOrThrow(_cursor, "villageId");
          final int _cursorIndexOfClan = CursorUtil.getColumnIndexOrThrow(_cursor, "clan");
          final int _cursorIndexOfEnrollmentStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "enrollmentStatus");
          final int _cursorIndexOfSupportStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStatus");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfConsentToMessages = CursorUtil.getColumnIndexOrThrow(_cursor, "consentToMessages");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final SupporterEntity _result;
          if (_cursor.moveToFirst()) {
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpGender;
            _tmpGender = _cursor.getString(_cursorIndexOfGender);
            final String _tmpAgeRange;
            _tmpAgeRange = _cursor.getString(_cursorIndexOfAgeRange);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpWard;
            _tmpWard = _cursor.getString(_cursorIndexOfWard);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpVillage;
            _tmpVillage = _cursor.getString(_cursorIndexOfVillage);
            final Integer _tmpVillageId;
            if (_cursor.isNull(_cursorIndexOfVillageId)) {
              _tmpVillageId = null;
            } else {
              _tmpVillageId = _cursor.getInt(_cursorIndexOfVillageId);
            }
            final String _tmpClan;
            _tmpClan = _cursor.getString(_cursorIndexOfClan);
            final String _tmpEnrollmentStatus;
            _tmpEnrollmentStatus = _cursor.getString(_cursorIndexOfEnrollmentStatus);
            final String _tmpSupportStatus;
            _tmpSupportStatus = _cursor.getString(_cursorIndexOfSupportStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final boolean _tmpConsentToMessages;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfConsentToMessages);
            _tmpConsentToMessages = _tmp_1 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _result = new SupporterEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpGender,_tmpAgeRange,_tmpPhone,_tmpWard,_tmpWardId,_tmpVillage,_tmpVillageId,_tmpClan,_tmpEnrollmentStatus,_tmpSupportStatus,_tmpNotes,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpConsentToMessages,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object getByServerId(final int serverId,
      final Continuation<? super SupporterEntity> $completion) {
    final String _sql = "SELECT * FROM supporters WHERE serverId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, serverId);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<SupporterEntity>() {
      @Override
      @Nullable
      public SupporterEntity call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfFullName = CursorUtil.getColumnIndexOrThrow(_cursor, "fullName");
          final int _cursorIndexOfGender = CursorUtil.getColumnIndexOrThrow(_cursor, "gender");
          final int _cursorIndexOfAgeRange = CursorUtil.getColumnIndexOrThrow(_cursor, "ageRange");
          final int _cursorIndexOfPhone = CursorUtil.getColumnIndexOrThrow(_cursor, "phone");
          final int _cursorIndexOfWard = CursorUtil.getColumnIndexOrThrow(_cursor, "ward");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfVillage = CursorUtil.getColumnIndexOrThrow(_cursor, "village");
          final int _cursorIndexOfVillageId = CursorUtil.getColumnIndexOrThrow(_cursor, "villageId");
          final int _cursorIndexOfClan = CursorUtil.getColumnIndexOrThrow(_cursor, "clan");
          final int _cursorIndexOfEnrollmentStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "enrollmentStatus");
          final int _cursorIndexOfSupportStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStatus");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfFollowUpRequired = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpRequired");
          final int _cursorIndexOfFollowUpDate = CursorUtil.getColumnIndexOrThrow(_cursor, "followUpDate");
          final int _cursorIndexOfConsentToMessages = CursorUtil.getColumnIndexOrThrow(_cursor, "consentToMessages");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final int _cursorIndexOfSyncStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "syncStatus");
          final int _cursorIndexOfCreatedLocallyAt = CursorUtil.getColumnIndexOrThrow(_cursor, "createdLocallyAt");
          final SupporterEntity _result;
          if (_cursor.moveToFirst()) {
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final Integer _tmpServerId;
            if (_cursor.isNull(_cursorIndexOfServerId)) {
              _tmpServerId = null;
            } else {
              _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            }
            final String _tmpFullName;
            _tmpFullName = _cursor.getString(_cursorIndexOfFullName);
            final String _tmpGender;
            _tmpGender = _cursor.getString(_cursorIndexOfGender);
            final String _tmpAgeRange;
            _tmpAgeRange = _cursor.getString(_cursorIndexOfAgeRange);
            final String _tmpPhone;
            _tmpPhone = _cursor.getString(_cursorIndexOfPhone);
            final String _tmpWard;
            _tmpWard = _cursor.getString(_cursorIndexOfWard);
            final Integer _tmpWardId;
            if (_cursor.isNull(_cursorIndexOfWardId)) {
              _tmpWardId = null;
            } else {
              _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            }
            final String _tmpVillage;
            _tmpVillage = _cursor.getString(_cursorIndexOfVillage);
            final Integer _tmpVillageId;
            if (_cursor.isNull(_cursorIndexOfVillageId)) {
              _tmpVillageId = null;
            } else {
              _tmpVillageId = _cursor.getInt(_cursorIndexOfVillageId);
            }
            final String _tmpClan;
            _tmpClan = _cursor.getString(_cursorIndexOfClan);
            final String _tmpEnrollmentStatus;
            _tmpEnrollmentStatus = _cursor.getString(_cursorIndexOfEnrollmentStatus);
            final String _tmpSupportStatus;
            _tmpSupportStatus = _cursor.getString(_cursorIndexOfSupportStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final boolean _tmpFollowUpRequired;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfFollowUpRequired);
            _tmpFollowUpRequired = _tmp != 0;
            final String _tmpFollowUpDate;
            if (_cursor.isNull(_cursorIndexOfFollowUpDate)) {
              _tmpFollowUpDate = null;
            } else {
              _tmpFollowUpDate = _cursor.getString(_cursorIndexOfFollowUpDate);
            }
            final boolean _tmpConsentToMessages;
            final int _tmp_1;
            _tmp_1 = _cursor.getInt(_cursorIndexOfConsentToMessages);
            _tmpConsentToMessages = _tmp_1 != 0;
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            final String _tmpSyncStatus;
            _tmpSyncStatus = _cursor.getString(_cursorIndexOfSyncStatus);
            final long _tmpCreatedLocallyAt;
            _tmpCreatedLocallyAt = _cursor.getLong(_cursorIndexOfCreatedLocallyAt);
            _result = new SupporterEntity(_tmpLocalId,_tmpServerId,_tmpFullName,_tmpGender,_tmpAgeRange,_tmpPhone,_tmpWard,_tmpWardId,_tmpVillage,_tmpVillageId,_tmpClan,_tmpEnrollmentStatus,_tmpSupportStatus,_tmpNotes,_tmpFollowUpRequired,_tmpFollowUpDate,_tmpConsentToMessages,_tmpUpdatedAt,_tmpSyncStatus,_tmpCreatedLocallyAt);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Object count(final Continuation<? super Integer> $completion) {
    final String _sql = "SELECT COUNT(*) FROM supporters";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<Integer>() {
      @Override
      @NonNull
      public Integer call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Integer _result;
          if (_cursor.moveToFirst()) {
            final int _tmp;
            _tmp = _cursor.getInt(0);
            _result = _tmp;
          } else {
            _result = 0;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
